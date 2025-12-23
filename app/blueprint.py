from flask_smorest import Api

from app.routers.user_router import blp as UserBlueprint
from app.routers.blog_router import blp as BlogBlueprint
from app.routers.conversation_router import blp as ConversationBlueprint
from app.routers.procedure_router import blp as ProcedureBlueprint
from app.routers.guest_router import blp as GuestBlueprint
from app.routers.transaction_router import blp as TransactionBlueprint
from app.routers.ai_usage_router import blp as AIUsageBlueprint


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
