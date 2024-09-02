from django.contrib import admin
from .models import Domain, CloudflareAPIKey

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'expiration_date', 'cloudflare_api_key', 'email')
    search_fields = ('domain_name',)
    list_filter = ('cloudflare_api_key',)

@admin.register(CloudflareAPIKey)
class CloudflareAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key')
    search_fields = ('name',)
