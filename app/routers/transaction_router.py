from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from app.schemas.transaction_schema import (
    TransactionSchema,
    TransactionCreateSchema,
    TransactionUpdateSchema,
    TransactionFilterSchema,
    TransactionPageSchema,
    TransactionCreateResponseSchema,
    MBBankWebhookSchema,
    WebhookResponseSchema,
    UpdateTransactionStatusSchema,
)
from app.services import transaction_service
from app.utils.decorators import permission_required
from app.services import user_service

blp = Blueprint("Transaction", __name__, description="Transaction API")


@blp.route("/transaction")
class TransactionList(MethodView):
    @jwt_required()
    @blp.arguments(TransactionFilterSchema, location="query")
    @blp.response(200, TransactionPageSchema)
    def get(self, filter_data):
        """Get all transactions with filtering and pagination
        - Admin: can view all transactions or filter by user_id
        - Regular user: can only view their own transactions
        """
        user_id = get_jwt_identity()
        current_user = user_service.get_user(user_id)

        is_admin = current_user.get("role") == 1  # Admin role

        result = transaction_service.get_all_transactions(
            filter_data=filter_data,
            user_id=user_id,
            is_admin=is_admin,
        )
        return result

@blp.route("/webhook/mbbank")
class MBBankWebhook(MethodView):
    @blp.arguments(MBBankWebhookSchema)
    @blp.response(200, WebhookResponseSchema)
    def post(self, webhook_data):
        print(webhook_data)
        """Process MBBank webhook notification and update transaction status

        This is a public endpoint for MBBank to notify payment completion.
        No authentication required as it comes from trusted banking system.
        """
        result = transaction_service.process_mbbank_webhook(webhook_data)
        return result



@blp.route("/transaction/<int:transaction_id>")
class Transaction(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        """Get a single transaction by ID"""
        # Check if user can access this transaction
        user_id = get_jwt_identity()
        current_user = user_service.get_user(user_id)
        transaction = transaction_service.get_transaction(transaction_id)

        # Admin can see all transactions, regular users can only see their own
        if current_user.role != 1 and transaction.user_id != user_id:
            abort(403, message="Access denied! You can only view your own transactions.")

        return transaction

    @jwt_required()
    @permission_required(permission_name="write")
    @blp.arguments(TransactionUpdateSchema)
    @blp.response(200, TransactionSchema)
    def put(self, transaction_data, transaction_id):
        """Update a transaction"""
        result = transaction_service.update_transaction(transaction_data, transaction_id)
        return result

    @jwt_required()
    @permission_required(permission_name="delete")
    def delete(self, transaction_id):
        """Delete a transaction"""
        result = transaction_service.delete_transaction(transaction_id)
        return result


@blp.route("/transaction/user/<int:user_id>")
class UserTransactions(MethodView):
    @jwt_required()
    @blp.arguments(TransactionFilterSchema, location="query")
    @blp.response(200, TransactionPageSchema)
    def get(self, filter_data, user_id):
        """Get all transactions for a specific user"""
        # Check if user can access transactions of the requested user
        current_user_id = get_jwt_identity()
        current_user = user_service.get_user(current_user_id)

        # Admin can see all users' transactions, regular users can only see their own
        if current_user.role != 1 and current_user_id != user_id:
            abort(403, message="Access denied! You can only view your own transactions.")

        result = transaction_service.get_user_transactions(user_id, filter_data)
        return result


@blp.route("/transaction/create")
class CreateTransaction(MethodView):
    @jwt_required()
    @blp.arguments(TransactionCreateSchema)
    @blp.response(201, TransactionCreateResponseSchema)
    def post(self, transaction_data):
        """Create a new transaction for current user"""
        user_id = get_jwt_identity()
        result = transaction_service.create_transaction(transaction_data, user_id)
        return result

@blp.route("/transaction/<string:transaction_id>")
class UpdateTransactionStatus(MethodView):
    @jwt_required()
    @blp.arguments(UpdateTransactionStatusSchema)
    @blp.response(200, TransactionSchema)
    def post(self, payload, transaction_id):
        """Update transaction status"""
        print(payload)
        status = payload["status"]
        result = transaction_service.update_transaction_status(transaction_id, status)
        return result


@blp.route("/user/<int:user_id>/balance")
class UserBalance(MethodView):
    @jwt_required()
    @permission_required(permission_name="read")
    def get(self, user_id):
        """Get user balance from transactions"""
        result = transaction_service.get_user_balance(user_id)
        return result


