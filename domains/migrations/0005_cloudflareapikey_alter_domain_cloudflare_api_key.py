# Generated by Django 4.2.15 on 2024-09-02 16:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0004_domain_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudflareAPIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A unique name for the API key', max_length=100, unique=True)),
                ('api_key', models.CharField(help_text='Your Cloudflare API key', max_length=40, unique=True, validators=[django.core.validators.MinLengthValidator(40), django.core.validators.MaxLengthValidator(40)])),
            ],
        ),
        migrations.AlterField(
            model_name='domain',
            name='cloudflare_api_key',
            field=models.ForeignKey(blank=True, help_text='Cloudflare API key used for DNS challenge', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='domains.cloudflareapikey'),
        ),
    ]