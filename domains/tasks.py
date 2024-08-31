from celery import shared_task
from domains.models import Domain
from django.utils import timezone
from datetime import timedelta
import asyncio
from telegram import Bot
from django.conf import settings
import subprocess
import os

@shared_task
def check_certificate_expiry():
    """
    Task to check for expiring certificates and send alerts to Telegram bot.
    """
    today = timezone.now().date()
    warning_date = today + timedelta(days=15)

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

@shared_task
def renew_certificates():
    """
    Task to renew SSL certificates for domains expiring in 7 days using Let's Encrypt and Cloudflare DNS challenge.
    """
    today = timezone.now().date()
    renewal_date = today + timedelta(days=7)

    # Fetch domains with certificates expiring in 7 days
    domains_to_renew = Domain.objects.filter(expiration_date__lte=renewal_date, expiration_date__gt=today)

    for domain in domains_to_renew:
        print(domain)
        if domain.cloudflare_api_key:
            renew_certificate(domain)


def renew_certificate(domain):
    """
    Renew the SSL certificate using Certbot and Cloudflare DNS challenge.
    """
    domain_name = domain.domain_name
    email = domain.email
    api_key = domain.cloudflare_api_key

    # Create a temporary credentials file for this specific renewal
    cloudflare_credentials_path = f"/tmp/cloudflare_{domain_name}.ini"
    
    with open(cloudflare_credentials_path, 'w') as f:
        f.write(f'dns_cloudflare_api_token = {api_key}')

    # Ensure the credentials file is not world-readable
    os.chmod(cloudflare_credentials_path, 0o600)

    # Command to run Certbot with DNS challenge using dynamic Cloudflare credentials
    certbot_command = [
        'certbot', 'certonly',
        '-d', domain_name,
        '-d', f'*.{domain_name}',
        '--dns-cloudflare',
        '--dns-cloudflare-credentials', cloudflare_credentials_path,
        '--non-interactive',
        '--agree-tos',
        '--email', email,
        '--force-renewal'
    ]

    try:
        subprocess.run(certbot_command, check=True)
        print(f"Successfully renewed certificate for {domain_name}")

        # Update the domain model with new certificate information
        update_domain_certificates(domain)

    except subprocess.CalledProcessError as e:
        print(f"Failed to renew certificate for {domain_name}: {e}")
    
    finally:
        # Clean up credentials file
        if os.path.exists(cloudflare_credentials_path):
            os.remove(cloudflare_credentials_path)


def update_domain_certificates(domain):
    """
    Update the Domain model instance with new certificate details.
    """
    # Define paths to Let's Encrypt certificate files for this domain
    cert_path = f'/etc/letsencrypt/live/{domain.domain_name}/cert.pem'
    privkey_path = f'/etc/letsencrypt/live/{domain.domain_name}/privkey.pem'
    chain_path = f'/etc/letsencrypt/live/{domain.domain_name}/chain.pem'
    fullchain_path = f'/etc/letsencrypt/live/{domain.domain_name}/fullchain.pem'

    try:
        with open(cert_path, 'r') as cert_file:
            domain.certificate = cert_file.read()

        with open(privkey_path, 'r') as privkey_file:
            domain.private_key = privkey_file.read()

        with open(chain_path, 'r') as chain_file:
            domain.chain = chain_file.read()

        with open(fullchain_path, 'r') as fullchain_file:
            domain.fullchain = fullchain_file.read()

        domain.save()
        print(f"Updated domain model with new certificate details for {domain.domain_name}")

    except FileNotFoundError as e:
        print(f"Error updating certificates for {domain.domain_name}: {e}")
