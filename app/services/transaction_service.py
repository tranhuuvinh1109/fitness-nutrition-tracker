import logging
from math import ceil

from flask_smorest import abort
from sqlalchemy import desc, and_

from app.db import db
from app.models.transaction_model import TransactionModel
from app.models.user_model import UserModel
from app.services import user_service
import uuid
from urllib.parse import quote
from sqlalchemy.orm import sessionmaker

# Create logger for this module
logger = logging.getLogger(__name__)

import re
from sqlalchemy.exc import SQLAlchemyError

TX_CODE_REGEX = re.compile(r"TX([A-Za-z0-9]{6,20})")

def get_all_transactions(filter_data=None, user_id=None, is_admin=False):
    """Get all transactions with role-based access control

    Args:
        filter_data: Query parameters for filtering
        user_id: Current user ID from JWT
        is_admin: Whether current user is admin (role = 1)

    Returns:
        Paginated transaction results based on user permissions
    """

    query = TransactionModel.query.filter(TransactionModel.deleted_at.is_(None))

    # 🔐 Permission check - Regular users can only see their own transactions
    if not is_admin:
        query = query.filter(TransactionModel.user_id == user_id)

    # 🔍 Apply filters (admin can filter by user_id, others can filter by status/payment_method)
    if filter_data:
        # Admin can filter by specific user_id
        if is_admin and filter_data.get("user_id"):
            query = query.filter(TransactionModel.user_id == filter_data["user_id"])

        # Both admin and regular users can filter by status and payment method
        if filter_data.get("status") is not None:
            query = query.filter(TransactionModel.status == filter_data["status"])

        if filter_data.get("payment_method"):
            query = query.filter(
                TransactionModel.payment_method == filter_data["payment_method"]
            )

    # 📄 Pagination
    page = filter_data.get("page", 1) if filter_data else 1
    page_size = filter_data.get("page_size", 20) if filter_data else 20

    total_transactions = query.count()
    total_page = ceil(total_transactions / page_size) if page_size else 1

    transactions = (
        query.order_by(desc(TransactionModel.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "results": transactions,
        "total_page": total_page,
        "total_transactions": total_transactions,
    }


def get_transaction(transaction_id):
    """Get a single transaction by ID"""
    transaction = TransactionModel.query.filter(TransactionModel.id == transaction_id, TransactionModel.deleted_at.is_(None)).first()
    if not transaction:
        logger.error(f"Transaction with id {transaction_id} not found")
        abort(404, message="Transaction not found")
    return transaction


def create_transaction(transaction_data, user_id):
    """Create a new transaction and return QR image URL"""
    try:
        transaction_id = str(uuid.uuid4())
        # Extract last part of UUID (after the last hyphen) as code
        transaction_code = transaction_id.split('-')[-1]  # Gets the last 12 characters
        amount = transaction_data["amount"]

        transaction = TransactionModel(
            id=transaction_id,
            user_id=user_id,
            status=transaction_data["status"],
            amount=amount,
            payment_method=transaction_data["payment_method"],
            additional_data=transaction_data.get("additional_data"),
            code=transaction_code,
        )

        db.session.add(transaction)
        db.session.commit()

        content = f"TX-{transaction_code}"
        # ✅ Generate VietQR image URL
        qr_image_url = (
            "https://img.vietqr.io/image/"
            "Mbbank-1663999999999-compact2.jpg"
            f"?amount={amount}"
            f"&addInfo={quote(content)}"
            "&accountName=Nguyen%20Nho%20Gia%20Huy"
        )

        logger.info(f"Transaction created successfully for user {user_id}")

        # ✅ Return data for FE
        return {
            "transaction": transaction,
            "qr_image_url": qr_image_url,
        }

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating transaction: {str(e)}")
        abort(500, message="Failed to create transaction")

def update_transaction(transaction_data, transaction_id):
    """Update an existing transaction"""
    transaction = TransactionModel.query.filter(TransactionModel.id == transaction_id, TransactionModel.deleted_at.is_(None)).first()
    if not transaction:
        logger.error(f"Transaction with id {transaction_id} not found")
        abort(404, message="Transaction not found")

    try:
        # Update fields if provided
        if "status" in transaction_data and transaction_data["status"] is not None:
            transaction.status = transaction_data["status"]

        if "amount" in transaction_data and transaction_data["amount"] is not None:
            transaction.amount = transaction_data["amount"]

        if "payment_method" in transaction_data and transaction_data["payment_method"]:
            transaction.payment_method = transaction_data["payment_method"]

        if "additional_data" in transaction_data:
            transaction.additional_data = transaction_data["additional_data"]

        db.session.commit()

        logger.info(f"Transaction {transaction_id} updated successfully")
        return transaction

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating transaction {transaction_id}: {str(e)}")
        abort(500, message="Failed to update transaction")


def delete_transaction(transaction_id):
    """Delete a transaction"""
    transaction = TransactionModel.query.filter(TransactionModel.id == transaction_id, TransactionModel.deleted_at.is_(None)).first()
    if not transaction:
        logger.error(f"Transaction with id {transaction_id} not found")
        abort(404, message="Transaction not found")

    try:
        db.session.delete(transaction)
        db.session.commit()

        logger.info(f"Transaction {transaction_id} deleted successfully")
        return {"message": "Transaction deleted successfully"}

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting transaction {transaction_id}: {str(e)}")
        abort(500, message="Failed to delete transaction")


def get_user_transactions(user_id, filter_data=None):
    """Get all transactions for a specific user"""
    query = TransactionModel.query.filter(TransactionModel.user_id == user_id, TransactionModel.deleted_at.is_(None))

    if filter_data:
        if filter_data.get("status") is not None:
            query = query.filter(TransactionModel.status == filter_data["status"])
        if filter_data.get("payment_method"):
            query = query.filter(TransactionModel.payment_method == filter_data["payment_method"])

    # Pagination
    page = filter_data.get("page", 1) if filter_data else 1
    page_size = filter_data.get("page_size", 20) if filter_data else 20

    total_transactions = query.count()
    total_page = ceil(total_transactions / page_size)

    transactions = query.order_by(desc(TransactionModel.created_at)) \
                       .offset((page - 1) * page_size) \
                       .limit(page_size) \
                       .all()

    return {
        "results": transactions,
        "total_page": total_page,
        "total_transactions": total_transactions
    }


def update_transaction_status(transaction_id, status):
    """Update transaction status"""
    transaction = TransactionModel.query.filter(
        TransactionModel.id == transaction_id,
        TransactionModel.deleted_at.is_(None)
    ).first()

    if not transaction:
        abort(404, message="Transaction not found")

    try:
        if transaction.status == 1 and status == 1:
            return transaction

        if status == 1: #completed
            user = UserModel.query.filter(
                UserModel.id == transaction.user_id,
                UserModel.deleted_at.is_(None)
            ).with_for_update().first()

            if not user:
                abort(404, message="User not found")

            user.balance += transaction.amount

        transaction.status = status
        db.session.commit()

        logger.info(
            f"Transaction {transaction_id} updated from {transaction.status} to {status}"
        )
        return transaction

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating transaction {transaction_id}: {str(e)}")
        abort(500, message="Failed to update transaction status")

def process_mbbank_webhook(webhook_data):
    logger.info(f"Received MBBank webhook: {webhook_data}")

    content = webhook_data.get("content", "")
    transfer_amount = webhook_data.get("transferAmount", 0)

    if not content:
        return {
            "success": False,
            "message": "Empty content",
            "transaction_code": None,
        }

    # 🔍 Extract transaction code from content (TX-xxxx)
    match = TX_CODE_REGEX.search(content)
    if not match:
        logger.warning(f"Transaction code not found in content: {content}")
        return {
            "success": False,
            "message": "Transaction code not found in content",
            "transaction_code": None,
        }

    transaction_code = match.group(1)
    logger.info(f"Extracted transaction code: {transaction_code}")

    try:
        # 🔎 Query by code (NOT id)
        transaction = TransactionModel.query.filter(TransactionModel.code == transaction_code, TransactionModel.deleted_at.is_(None)).first()
        

        if not transaction:
            logger.warning(f"Transaction not found with code: {transaction_code}")
            return {
                "success": False,
                "message": f"Transaction not found: {transaction_code}",
                "transaction_code": transaction_code,
            }

        # 💰 Validate amount
        if abs(transaction.amount - transfer_amount) > 0.01:
            logger.warning(
                f"Amount mismatch for TX-{transaction_code}: "
                f"expected {transaction.amount}, got {transfer_amount}"
            )
            return {
                "success": False,
                "message": "Amount mismatch",
                "transaction_code": transaction_code,
            }
        # get user from transaction.user_id and add transaction.amount into balance for this user
        user = UserModel.query.filter(UserModel.id == transaction.user_id, UserModel.deleted_at.is_(None)).first()
        if not user:
            logger.error(f"User with id {transaction.user_id} not found")
            return {
                "success": False,
                "message": "User not found",
                "transaction_code": transaction_code,
            }

        # ✅ Already completed
        if transaction.status == 1:
            return {
                "success": True,
                "message": "Transaction already completed",
                "transaction_code": transaction_code,
            }

        # 🔄 Update status and user balance
        user.balance += transaction.amount
        transaction.status = 1
        db.session.commit()

        logger.info(f"Transaction TX-{transaction_code} completed")

        return {
            "success": True,
            "message": "Transaction completed successfully",
            "transaction_code": transaction_code,
        }

    except Exception as e:
        db.session.rollback()
        logger.error(f"Webhook processing error: {str(e)}")
        return {
            "success": False,
            "message": "Internal server error",
            "transaction_code": transaction_code,
        }


def get_user_balance(user_id):
    """Calculate user balance from completed transactions"""
    user = UserModel.query.filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()
    if not user:
        abort(404, message="User not found")

    # Sum of all completed transactions (status = 1)
    completed_transactions = TransactionModel.query.filter(
        TransactionModel.user_id == user_id, TransactionModel.status == 1, TransactionModel.deleted_at.is_(None)
    ).all()

    balance = sum(transaction.amount for transaction in completed_transactions)
    return {"user_id": user_id, "balance": balance, "stored_balance": user.balance}
