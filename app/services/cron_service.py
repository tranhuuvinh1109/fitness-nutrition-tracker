from app.services.mail_service import send_email
import os
import logging

logger = logging.getLogger(__name__)

def send_daily_report():
    """
    Cron job to send daily report email.
    """
    target_email = os.environ.get("CRON_TARGET_EMAIL")
    if not target_email:
        logger.warning("CRON_TARGET_EMAIL not set, skipping daily email job.")
        return

    logger.info(f"Sending daily report to {target_email}...")
    
    # Vietnamese content
    subject = "Báo cáo Fitness Tracker Hàng Ngày"
    content = """
    <h1>Lời nhắc hàng ngày</h1>
    <p>Đừng quên ghi lại nhật ký ăn uống và tập luyện hôm nay nhé!</p>
    <p>Hãy kiểm tra ứng dụng để xem các gợi ý mới nhất.</p>
    <a href="https://fitness-ai-umber.vercel.app/">Mở ứng dụng</a>
    """
    
    try:
        result = send_email(target_email, subject, content)
        logger.info(f"Daily email sent result: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to send daily email: {e}")
