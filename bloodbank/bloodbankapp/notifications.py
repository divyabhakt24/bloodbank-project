# notifications.py
from django.core import mail
import logging

logger = logging.getLogger(__name__)


def send_donation_initiated_notification(donation):
    try:
        # ... (your existing email composition code)

        connection = mail.get_connection()
        connection.open()  # Explicitly open connection
        email = mail.EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [donation.donor.email],
            connection=connection,
        )
        email.send()
        connection.close()  # Close connection

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        # Optionally notify admins
        mail.mail_admins(
            "Email sending failed",
            f"Failed to send donation notification: {str(e)}"
        )