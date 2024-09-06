from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module for 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sslkeeper.settings')

# Create an instance of the Celery application.
app = Celery('sslkeeper')

# Configure Celery using Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-certificate-expiry-every-day': {
        'task': 'domains.tasks.check_certificate_expiry',
        'schedule': crontab(hour=0, minute=0),  # Run once a day at midnight
    },
    'renew-certificates-every-hour': {
        'task': 'domains.tasks.renew_certificates',
        'schedule': crontab(minute=0, hour='*'),  # Runs every hour
    },
}
