from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.chat_schema import ConversationSchema, ConversationCreateSchema, ConversationUpdateSchema, ChatMessageSchema, ChatMessageAskSchema
from app.services.conversation_service import conversation_service
from app.services.chat_service import chat_service

blp = Blueprint("Conversation", __name__, description="Conversation API")


@blp.route("/conversation")
class ConversationList(MethodView):
    @jwt_required()
    @blp.response(200, ConversationSchema(many=True))
    def get(self):
        """Get all conversations of current user"""
        user_id = get_jwt_identity()
        return conversation_service.get_all(user_id)

    @jwt_required()
    @blp.arguments(ConversationCreateSchema)
    @blp.response(201, ConversationSchema)
    def post(self, data):
        """Create a new conversation for current user"""
        user_id = get_jwt_identity()
        title = data.get("title")
        return conversation_service.create(user_id, title)

@blp.route("/conversation/<string:conversation_id>")
class ConversationDetail(MethodView):
    @blp.response(200, ConversationSchema)
    def get(self, conversation_id):
        """Get conversation details by ID"""
        conversation = conversation_service.get(conversation_id)
        if not conversation:
            abort(404, message=f"Conversation {conversation_id} not found")
        return conversation

    @blp.arguments(ConversationUpdateSchema)
    @blp.response(200, ConversationSchema)
    def put(self, data, conversation_id):
        """Update conversation"""
        return conversation_service.update(conversation_id, data)

    @blp.response(204)
    def delete(self, conversation_id):
        """Delete conversation"""
        conversation_service.delete(conversation_id)
        return {}

@blp.route("/conversation/<string:conversation_id>/messages")
class ConversationMessages(MethodView):
    @blp.response(200, ChatMessageSchema(many=True))
    def get(self, conversation_id):
        """Get all messages in a conversation"""
        messages = chat_service.get_all_messages_by_conversation(conversation_id)
        return messages

@blp.route("/conversation/<string:conversation_id>/ask")
class ConversationAskAI(MethodView):
    @jwt_required()
    @blp.arguments(ChatMessageAskSchema)
    @blp.response(201, ChatMessageSchema)
    def post(self, data, conversation_id):
        """
        User gửi tin nhắn đến AI, fake trả lời từ bot, lưu cả 2 message
        Body:
        {
            "message": "Nội dung câu hỏi",
            "metadata": {} (optional)
        }
        """
        user_id = get_jwt_identity()  # Lấy user_id từ token
        message_text = data.get("message")
        model = data.get("model")

        if not message_text:
            abort(400, message="message là bắt buộc")

        # Gọi service để fake AI trả lời
        bot_message = conversation_service.ask_ai(
            conversation_id=conversation_id,
            user_id=user_id,
            message_text=message_text,
            model=model
        )

        return bot_message