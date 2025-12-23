from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.water_log_schema import (
    WaterLogCreateSchema,
    WaterLogResponseSchema,
    WaterLogUpdateSchema
)
from app.services import water_log_service

blp = Blueprint("WaterLog", __name__, description="Water Log API")


@blp.route("/water-logs")
class WaterLogList(MethodView):
    @jwt_required()
    @blp.response(200, WaterLogResponseSchema(many=True))
    def get(self):
        """Get all water logs for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        log_date = self.request.args.get('log_date')
        result = water_log_service.get_all_water_logs(user_id=user_id, log_date=log_date)
        return result

    @jwt_required()
    @blp.arguments(WaterLogCreateSchema)
    @blp.response(201, WaterLogResponseSchema)
    def post(self, water_log_data):
        """Create a new water log for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = water_log_service.create_water_log(user_id, water_log_data)
        return result


@blp.route("/water-logs/<water_log_id>")
class WaterLog(MethodView):
    @jwt_required()
    @blp.response(200, WaterLogResponseSchema)
    def get(self, water_log_id):
        """Get water log by ID"""
        result = water_log_service.get_water_log(water_log_id)

        # Check if user owns this water log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(result.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        return result

    @jwt_required()
    @blp.arguments(WaterLogUpdateSchema)
    @blp.response(200, WaterLogResponseSchema)
    def put(self, water_log_data, water_log_id):
        """Update water log by ID"""
        water_log = water_log_service.get_water_log(water_log_id)

        # Check if user owns this water log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(water_log.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = water_log_service.update_water_log(water_log_id, water_log_data)
        return result

    @jwt_required()
    @blp.response(200)
    def delete(self, water_log_id):
        """Delete water log by ID"""
        water_log = water_log_service.get_water_log(water_log_id)

        # Check if user owns this water log
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(water_log.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = water_log_service.delete_water_log(water_log_id)
        return result


@blp.route("/water-logs/total/<date>")
class WaterLogTotal(MethodView):
    @jwt_required()
    @blp.response(200)
    def get(self, date):
        """Get total water intake for current user on a specific date"""
        from flask_jwt_extended import get_jwt_identity
        from datetime import datetime
        user_id = get_jwt_identity()

        try:
            log_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            from flask_smorest import abort
            abort(400, message="Invalid date format. Use YYYY-MM-DD")

        total = water_log_service.get_total_water_for_date(user_id, log_date)
        return {"date": date, "total_ml": total}
