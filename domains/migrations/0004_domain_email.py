# Generated by Django 4.2.15 on 2024-08-31 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0003_domain_chain_domain_fullchain'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]