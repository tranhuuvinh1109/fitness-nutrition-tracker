import json
import logging
import os
from datetime import date, datetime, timedelta

from flask_smorest import abort
from openai import OpenAI

from app.db import db
from app.models.food_log_model import FoodLogModel
from app.models.enums import MealTypeEnum
from app.services import user_profile_service

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


def suggest_food_plan(user_id, day_plan=None, meal_type=None):
    """
    Suggest a personalized food plan for a user
    If day_plan is provided, suggest for that specific date.
    Otherwise, suggest for today.
    If meal_type is provided, suggest only for that meal.
    """
    # Get user profile
    user_profile = user_profile_service.get_user_profile(user_id)
    if not user_profile:
        logger.error(f"User profile not found for user_id: {user_id}")
        abort(404, message="User profile not found. Please create your profile first.")

    # Determine target date
    if day_plan:
        try:
            target_date = datetime.strptime(day_plan, "%Y-%m-%d").date()
        except ValueError:
            logger.error(f"Invalid date format for day_plan: {day_plan}")
            abort(400, message="Invalid date format. Please use YYYY-MM-DD")
    else:
        target_date = date.today()

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

    # Get recent food logs to avoid duplication (last 7 days + today)
    start_date = target_date - timedelta(days=7)
    recent_logs = FoodLogModel.query.filter(
        FoodLogModel.user_id == user_id,
        FoodLogModel.log_date >= start_date,
        FoodLogModel.log_date <= target_date
    ).all()
    
    recent_food_names = list(set([log.name for log in recent_logs]))
    recent_foods_str = ", ".join(recent_food_names) if recent_food_names else "Chưa có món ăn nào"

    # Specific meal type prompt addition
    meal_type_prompt = ""
    if meal_type:
        meal_type_value = meal_type.value if hasattr(meal_type, 'value') else meal_type
        meal_type_prompt = f"- Chỉ đề xuất món ăn cho bữa: {meal_type_value}"

    # Create prompt for OpenAI
    prompt = f"""Bạn là một chuyên gia dinh dưỡng thể hình am hiểu ẩm thực Việt Nam (Healthy/Eat Clean). Hãy đề xuất **01 món ăn Việt Nam** KHỎE MẠNH (Healthy), phù hợp cho người tập GYM vào lúc này dựa trên thông tin sau:

Thông tin người dùng:
- Tuổi: {user_info['age']}
- Giới tính: {user_info['gender']}
- Chiều cao: {user_info['height_cm']} cm
- Cân nặng: {user_info['weight_kg']} kg
- BMI: {user_info['bmi']}
- Mức độ hoạt động: {user_info['activity_level']}
- Mục tiêu: {json.dumps(user_info['target'], ensure_ascii=False) if user_info['target'] else 'Không có'}
- Các món đã ăn trong 7 ngày qua (HÃY TRÁNH GỢI Ý LẠI): {recent_foods_str}
{meal_type_prompt}

Hãy trả về kết quả dưới dạng JSON sau:
{{
    "foods": [
        {{
            "name": "<tên món ăn tiếng Việt>",
            "meal_type": "<breakfast|lunch|dinner|snack>",
            "calories": <calo ước tính>,
            "protein": <protein (g)>,
            "carbs": <carbs (g)>,
            "fat": <fat (g)>,
            "description": "<mô tả ngắn về món ăn và nguyên liệu chính, nhấn mạnh yếu tố healthy>"
        }}
    ]
}}

Lưu ý:
- Chỉ đề xuất SỐ LƯỢNG ĐÚNG 1 MÓN ĂN.
- Món ăn phải là món Việt Nam nhưng được chế biến theo phong cách Healthy/Eat Clean (ít dầu mỡ, ít đường, ít gia vị mặn).
- Ưu tiên thực phẩm giàu Protein và chất xơ.
- KHÔNG ĐƯỢC trùng với các món đã ăn trong 7 ngày qua (đã liệt kê ở trên).
- Tự động xác định bữa ăn (meal_type) phù hợp.
{'- Đảm bảo món ăn phù hợp với bữa: ' + (meal_type.value if hasattr(meal_type, 'value') else str(meal_type)) if meal_type else ''}
- Đảm bảo dinh dưỡng phù hợp với mục tiêu thể hình của người dùng.
- Trả về chỉ JSON, không có text thêm."""

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là một chuyên gia dinh dưỡng. Trả về chỉ JSON, không có text thêm."
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
        food_plan = json.loads(response_content)

        # Validate response structure
        if "foods" not in food_plan:
            logger.error("Invalid food plan structure from OpenAI")
            abort(500, message="Invalid food plan structure received from AI")

        # Process foods and create food logs
        created_food_items = []
        created_logs = []
        
        # Limit to 1 item just in case AI returns more
        for food_data in food_plan["foods"][:1]:
            # Validate required fields
            required_fields = ["name", "meal_type", "calories"]
            if not all(field in food_data for field in required_fields):
                logger.error(f"Missing required fields in food data: {food_data}")
                continue

            # Validate meal type
            if meal_type:
                meal_type_enum = meal_type
                meal_type_str = meal_type.value
            else:
                try:
                    meal_type_str = food_data["meal_type"].lower()
                    meal_type_enum = MealTypeEnum(meal_type_str)
                except (ValueError, AttributeError) as e:
                    logger.error(f"Invalid meal type: {food_data.get('meal_type')}, error: {e}")
                    continue

            # check exist
            existing_log = FoodLogModel.query.filter_by(
                user_id=user_id,
                log_date=target_date,
                meal_type=meal_type_enum,
                name=food_data["name"]
            ).first()

            if not existing_log:
                food_log = FoodLogModel(
                    user_id=user_id,
                    log_date=target_date,
                    meal_type=meal_type_enum,
                    name=food_data["name"],
                    calories=food_data["calories"],
                    protein=food_data.get("protein"),
                    carbs=food_data.get("carbs"),
                    fat=food_data.get("fat"),
                    quantity=1.0  # Default quantity
                )
                db.session.add(food_log)
                created_logs.append(food_log)
            else:
                existing_log.calories = food_data["calories"]
                existing_log.protein = food_data.get("protein")
                existing_log.carbs = food_data.get("carbs")
                existing_log.fat = food_data.get("fat")
                existing_log.quantity = 1.0
                created_logs.append(existing_log)

            created_food_items.append({
                "log": created_logs[-1],
                "name": food_data["name"],
                "meal_type": meal_type_str,
                "calories": food_data["calories"],
                "description": food_data.get("description", "")
            })

        # Commit all changes
        db.session.commit()

        logger.info(f"Food plan created successfully for user_id: {user_id} on {target_date}")
        
        return {
            "date": target_date.isoformat(),
            "foods": created_food_items
        }

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI response: {e}")
        db.session.rollback()
        abort(500, message="Failed to parse AI response")
    except Exception as e:
        logger.error(f"Failed to generate food plan: {e}")
        db.session.rollback()
        abort(500, message=f"Failed to generate food plan: {str(e)}")
