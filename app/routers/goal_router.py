from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.goal_schema import (
    GoalCreateSchema,
    GoalResponseSchema,
    GoalUpdateSchema
)
from app.services import goal_service

blp = Blueprint("Goal", __name__, description="Goal API")


@blp.route("/goals")
class GoalList(MethodView):
    @jwt_required()
    @blp.response(200, GoalResponseSchema(many=True))
    def get(self):
        """Get all goals for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = goal_service.get_all_goals(user_id=user_id)
        return result

    @jwt_required()
    @blp.arguments(GoalCreateSchema)
    @blp.response(201, GoalResponseSchema)
    def post(self, goal_data):
        """Create a new goal for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = goal_service.create_goal(user_id, goal_data)
        return result


@blp.route("/goals/<goal_id>")
class Goal(MethodView):
    @jwt_required()
    @blp.response(200, GoalResponseSchema)
    def get(self, goal_id):
        """Get goal by ID"""
        result = goal_service.get_goal(goal_id)

        # Check if user owns this goal
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(result.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        return result

    @jwt_required()
    @blp.arguments(GoalUpdateSchema)
    @blp.response(200, GoalResponseSchema)
    def put(self, goal_data, goal_id):
        """Update goal by ID"""
        goal = goal_service.get_goal(goal_id)

        # Check if user owns this goal
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(goal.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = goal_service.update_goal(goal_id, goal_data)
        return result

    @jwt_required()
    @blp.response(200)
    def delete(self, goal_id):
        """Delete goal by ID"""
        goal = goal_service.get_goal(goal_id)

        # Check if user owns this goal
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(goal.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = goal_service.delete_goal(goal_id)
        return result
