from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.schemas.ai_message_schema import (
    AIMessageCreateSchema,
    AIMessageResponseSchema,
    AIMessageUpdateSchema,
    AIMessageAskSchema
)
from app.services import ai_message_service

blp = Blueprint("AIMessage", __name__, description="AI Message API")


@blp.route("/ai-messages/ask")
class AIMessageAsk(MethodView):
    @jwt_required()
    @blp.arguments(AIMessageAskSchema)
    @blp.response(200, AIMessageResponseSchema)
    def post(self, ask_data):
        """Ask AI a question and get response with user profile context"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        
        result = ai_message_service.ask_ai(user_id, ask_data["message"])
        return result


@blp.route("/ai-messages")
class AIMessageList(MethodView):
    @jwt_required()
    @blp.response(200, AIMessageResponseSchema(many=True))
    def get(self):
        """Get all AI messages for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = ai_message_service.get_all_ai_messages(user_id=user_id)
        return result

    @jwt_required()
    @blp.arguments(AIMessageCreateSchema)
    @blp.response(201, AIMessageResponseSchema)
    def post(self, ai_message_data):
        """Create a new AI message for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = ai_message_service.create_ai_message(user_id, ai_message_data)
        return result


@blp.route("/ai-messages/<ai_message_id>")
class AIMessage(MethodView):
    @jwt_required()
    @blp.response(200, AIMessageResponseSchema)
    def get(self, ai_message_id):
        """Get AI message by ID"""
        result = ai_message_service.get_ai_message(ai_message_id)

        # Check if user owns this AI message
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(result.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        return result

    @jwt_required()
    @blp.arguments(AIMessageUpdateSchema)
    @blp.response(200, AIMessageResponseSchema)
    def put(self, ai_message_data, ai_message_id):
        """Update AI message by ID"""
        ai_message = ai_message_service.get_ai_message(ai_message_id)

        # Check if user owns this AI message
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(ai_message.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = ai_message_service.update_ai_message(ai_message_id, ai_message_data)
        return result

    @jwt_required()
    @blp.response(200)
    def delete(self, ai_message_id):
        """Delete AI message by ID"""
        ai_message = ai_message_service.get_ai_message(ai_message_id)

        # Check if user owns this AI message
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        if str(ai_message.user_id) != current_user_id:
            from flask_smorest import abort
            abort(403, message="Access denied")

        result = ai_message_service.delete_ai_message(ai_message_id)
        return result


@blp.route("/ai-messages/conversation")
class AIConversation(MethodView):
    @jwt_required()
    @blp.response(200, AIMessageResponseSchema(many=True))
    def get(self):
        """Get conversation history for current user"""
        from flask_jwt_extended import get_jwt_identity
        from flask import request
        user_id = get_jwt_identity()

        limit = request.args.get('limit', 50, type=int)
        result = ai_message_service.get_conversation_history(user_id, limit=limit)
        return result

    @jwt_required()
    @blp.response(200)
    def delete(self):
        """Delete all AI messages (conversation history) for current user"""
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()

        result = ai_message_service.delete_conversation_history(user_id)
        return result
