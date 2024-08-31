from celery import shared_task
from domains.models import Domain
from django.utils import timezone
from datetime import timedelta
import asyncio
from telegram import Bot
from django.conf import settings

@shared_task
def check_certificate_expiry():
    """
    Task to check for expiring certificates and send alerts to Telegram bot.
    """
    today = timezone.now().date()
    warning_date = today + timedelta(days=500)

    # Find domains with certificates expiring within 15 days
    expiring_domains = Domain.objects.filter(expiration_date__lte=warning_date, expiration_date__gt=today)

    if expiring_domains:
        send_telegram_alert(expiring_domains)


def send_telegram_alert(domains):
    """
    Send an alert message to a Telegram bot for domains with expiring certificates.
    """

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID

    for domain in domains:
        message = (
            f"Alert: The SSL certificate for domain {domain.domain_name} "
            f"is expiring on {domain.expiration_date}. Please renew it as soon as possible."
        )
        asyncio.run(bot.send_message(chat_id=chat_id, text=message))
