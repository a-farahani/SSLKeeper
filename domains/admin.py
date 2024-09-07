from django.contrib import admin
from .models import Domain, CloudflareAPIKey
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from domains.tasks import generate_certificate

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'expiration_date', 'cloudflare_api_key', 'email', 'generate_certificate_button')
    search_fields = ('domain_name',)
    list_filter = ('cloudflare_api_key',)

    def generate_certificate_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Generate Certificate</a>',
            f'/admin/domains/domain/{obj.id}/generate_certificate/'
        )
    generate_certificate_button.short_description = 'Generate Certificate'
    generate_certificate_button.allow_tags = True

    # Add a custom URL in the admin for triggering the task
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:domain_id>/generate_certificate/',
                self.admin_site.admin_view(self.generate_certificate),
                name='generate-certificate',
            ),
        ]
        return custom_urls + urls

    # Custom view for generating certificate
    def generate_certificate(self, request, domain_id):
        # Trigger the Celery task
        generate_certificate.delay(domain_id)
        self.message_user(request, f"Certificate generation task started for domain ID {domain_id}")
        return redirect(f'/admin/domains/domain/')

@admin.register(CloudflareAPIKey)
class CloudflareAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key')
    search_fields = ('name',)
