from django.contrib import admin
from .models import Domain

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'expiration_date', 'cloudflare_api_key')
    search_fields = ('domain_name',)
    readonly_fields = ('expiration_date',)
