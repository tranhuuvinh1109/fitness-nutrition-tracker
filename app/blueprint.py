from flask_smorest import Api

from app.routers.user_router import blp as UserBlueprint
from app.routers.blog_router import blp as BlogBlueprint
from app.routers.conversation_router import blp as ConversationBlueprint
from app.routers.procedure_router import blp as ProcedureBlueprint
from app.routers.guest_router import blp as GuestBlueprint
from app.routers.transaction_router import blp as TransactionBlueprint
from app.routers.ai_usage_router import blp as AIUsageBlueprint
from app.routers.user_profile_router import blp as UserProfileBlueprint
from app.routers.goal_router import blp as GoalBlueprint
from app.routers.food_router import blp as FoodBlueprint
from app.routers.food_log_router import blp as FoodLogBlueprint
from app.routers.workout_router import blp as WorkoutBlueprint
from app.routers.workout_log_router import blp as WorkoutLogBlueprint
from app.routers.water_log_router import blp as WaterLogBlueprint
from app.routers.ai_message_router import blp as AIMessageBlueprint


# Register Blueprint
def register_routing(app):
    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(BlogBlueprint)
    api.register_blueprint(ConversationBlueprint)
    api.register_blueprint(ProcedureBlueprint)
    api.register_blueprint(GuestBlueprint)
    api.register_blueprint(TransactionBlueprint)
    api.register_blueprint(AIUsageBlueprint)
    api.register_blueprint(UserProfileBlueprint)
    api.register_blueprint(GoalBlueprint)
    api.register_blueprint(FoodBlueprint)
    api.register_blueprint(FoodLogBlueprint)
    api.register_blueprint(WorkoutBlueprint)
    api.register_blueprint(WorkoutLogBlueprint)
    api.register_blueprint(WaterLogBlueprint)
    api.register_blueprint(AIMessageBlueprint)
