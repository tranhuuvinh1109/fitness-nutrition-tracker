import json
import logging
import os
from datetime import date, datetime, timedelta

from flask_smorest import abort
from openai import OpenAI

from app.db import db
from app.models.workout_log_model import WorkoutLogModel
from app.models.enums import WorkoutTypeEnum
from app.services import user_profile_service, workout_service, workout_log_service

# Create logger for this module
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = None


def get_openai_client():
    """Initialize and return OpenAI client"""
    global openai_client
    if openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            abort(500, message="OpenAI API key not configured")
        openai_client = OpenAI(api_key=api_key)
    return openai_client


def suggest_workout_plan(user_id, start_date=None, end_date=None):
    """
    Suggest a personalized workout plan for a user based on their profile
    Returns a workout plan with sessions per week and exercises
    """
    # Parse dates if provided, otherwise default to current week (Monday to Sunday)
    today = date.today()
    if start_date:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        # Default to Monday of current week
        days_since_monday = today.weekday()
        start_date = today - timedelta(days=days_since_monday)

    if end_date:
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date = end_date
    else:   
        # Default to Sunday of the same week as start_date
        end_date = start_date + timedelta(days=6)

    # Get user profile
    user_profile = user_profile_service.get_user_profile(user_id)
    if not user_profile:
        logger.error(f"User profile not found for user_id: {user_id}")
        abort(404, message="User profile not found. Please create your profile first.")

    # Prepare user information for OpenAI
    user_info = {
        "age": user_profile.age,
        "gender": user_profile.gender.value if user_profile.gender else None,
        "height_cm": user_profile.height_cm,
        "weight_kg": user_profile.weight_kg,
        "bmi": user_profile.bmi,
        "activity_level": user_profile.activity_level.value if user_profile.activity_level else None,
        "target": user_profile.target
    }

    # Create prompt for OpenAI
    prompt = f"""Bạn là một chuyên gia thể dục và dinh dưỡng. Hãy đề xuất một kế hoạch tập luyện cá nhân hóa dựa trên thông tin sau:

Thông tin người dùng:
- Tuổi: {user_info['age']}
- Giới tính: {user_info['gender']}
- Chiều cao: {user_info['height_cm']} cm
- Cân nặng: {user_info['weight_kg']} kg
- BMI: {user_info['bmi']}
- Mức độ hoạt động: {user_info['activity_level']}
- Mục tiêu: {json.dumps(user_info['target'], ensure_ascii=False) if user_info['target'] else 'Không có'}

Kế hoạch tập luyện trong khoảng thời gian từ {start_date} đến {end_date}.

Hãy trả về kế hoạch tập luyện với định dạng JSON sau:
{{
    "sessions_per_week": <số buổi tập trong tuần (3-7)>,
    "workouts": [
        {{
            "name": "<tên bài tập>",
            "type": "<cardio|strength|flexibility>",
            "duration_min": <thời gian tập (phút)>,
            "calories_burned": <calo đốt cháy ước tính>,
            "log_date": "<YYYY-MM-DD>",
            "description": "<mô tả chi tiết bài tập>",
            "link_reference": "<URL string (YouTube hoặc blog). Nếu không có thì null>"
        }}
    ]
}}

Lưu ý:
- Mỗi bài tập phải có type là một trong: cardio, strength, flexibility
- Phân bổ đều các buổi tập trong khoảng thời gian yêu cầu.
- log_date phải nằm trong khoảng từ {start_date} đến {end_date}.
- link_reference PHẢI là một link video hướng dẫn trên YouTube (nếu có thể tìm được chính xác).
- Đảm bảo phù hợp với mục tiêu và tình trạng sức khỏe của người dùng
- Trả về chỉ JSON, không có text thêm"""

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là một chuyên gia thể dục. Trả về chỉ JSON, không có text thêm."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        # Parse response
        response_content = response.choices[0].message.content
        workout_plan = json.loads(response_content)

        # Validate response structure
        if "sessions_per_week" not in workout_plan or "workouts" not in workout_plan:
            logger.error("Invalid workout plan structure from OpenAI")
            abort(500, message="Invalid workout plan structure received from AI")

        # Process workouts and create workout logs
        created_workouts = []
        created_logs = []
        
        for workout_data in workout_plan["workouts"]:
            # Validate required fields
            required_fields = ["name", "type", "duration_min", "log_date"]
            if not all(field in workout_data for field in required_fields):
                logger.error(f"Missing required fields in workout data: {workout_data}")
                continue  # Skip this workout if required fields are missing

            # Validate workout type and convert to integer
            try:
                workout_type_str = workout_data["type"].lower()
                workout_type_enum = WorkoutTypeEnum(workout_type_str)
                # Map enum to integer: 0: cardio, 1: strength, 2: flexibility
                workout_type_map = {
                    WorkoutTypeEnum.cardio: 0,
                    WorkoutTypeEnum.strength: 1,
                    WorkoutTypeEnum.flexibility: 2
                }
                workout_type_int = workout_type_map.get(workout_type_enum, 0)
            except (ValueError, AttributeError) as e:
                logger.error(f"Invalid workout type: {workout_data.get('type')}, error: {e}")
                continue  # Skip this workout if type is invalid

            # Parse log date from AI response
            try:
                workout_log_date = datetime.strptime(workout_data["log_date"], '%Y-%m-%d').date()
            except ValueError:
                logger.error(f"Invalid log date format from AI: {workout_data['log_date']}")
                continue

            link_reference = workout_data.get("link_reference")
            if link_reference and not isinstance(link_reference, str):
                link_reference = None                                           

            # Prepare workout metadata
            workout_metadata = {
                "name": workout_data["name"],
                "description": workout_data.get("description", ""),
                "link_reference": link_reference
            }

            # Check if workout log already exists for this date and workout type
            existing_log = WorkoutLogModel.query.filter_by(
                user_id=user_id,
                log_date=workout_log_date,
                workout_type=workout_type_int
            ).first()

            if not existing_log:
                # Create workout log
                workout_log = WorkoutLogModel(
                    user_id=user_id,
                    duration_min=workout_data["duration_min"],
                    calories_burned=workout_data.get("calories_burned"),
                    log_date=workout_log_date,
                    status=0,  # Default to planned
                    workout_type=workout_type_int,
                    workout_metadata=workout_metadata,
                    description=workout_data.get("description", "")
                )
                db.session.add(workout_log)
                created_logs.append(workout_log)
            else:
                # Update existing log
                existing_log.duration_min = workout_data["duration_min"]
                existing_log.calories_burned = workout_data.get("calories_burned")
                existing_log.workout_type = workout_type_int
                existing_log.workout_metadata = workout_metadata
                existing_log.description = workout_data.get("description", "")
                created_logs.append(existing_log)

            created_workouts.append({
                "log": created_logs[-1] if created_logs else None,
                "name": workout_data["name"],
                "type": workout_data["type"],
                "description": workout_data.get("description", ""),
                "log_date": workout_data["log_date"],
                "link_reference": workout_data.get("link_reference")
            })

        # Commit all changes
        db.session.commit()

        logger.info(f"Workout plan created successfully for user_id: {user_id}")
        
        return {
            "sessions_per_week": workout_plan["sessions_per_week"],
            "start_date": start_date.isoformat(),
            "workouts": created_workouts
        }

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI response: {e}")
        db.session.rollback()
        abort(500, message="Failed to parse AI response")
    except Exception as e:
        logger.error(f"Failed to generate workout plan: {e}")
        db.session.rollback()
        abort(500, message=f"Failed to generate workout plan: {str(e)}")
