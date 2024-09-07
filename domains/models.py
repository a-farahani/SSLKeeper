from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from cryptography import x509
from cryptography.hazmat.backends import default_backend

class CloudflareAPIKey(models.Model):
    """
    Model to store Cloudflare API keys.
    """
    name = models.CharField(max_length=100, unique=True, help_text="A unique name for the API key")
    api_key = models.CharField(
        max_length=40,
        unique=True,
        validators=[MinLengthValidator(40), MaxLengthValidator(40)],
        help_text="Your Cloudflare API key"
    )

    def __str__(self):
        return self.name
    

class LongTextField(models.TextField):
    """
    Custom model field for LongTextField to handle very large text data.
    """
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'LONGTEXT'
        else:
            return super().db_type(connection)


def validate_certificate(value):
    """
    Custom validator to check if the certificate is valid and extract expiration date.
    """
    try:
        cert = x509.load_pem_x509_certificate(value.encode(), default_backend())
        return cert.not_valid_after
    except Exception as e:
        raise ValidationError(f"Invalid certificate content: {e}")


class Domain(models.Model):
    """
    Model to store Domains.
    """
    domain_name = models.CharField(max_length=255, unique=True)
    private_key = LongTextField(blank=True, null=True)
    certificate = LongTextField(blank=True, null=True, validators=[validate_certificate])
    chain = LongTextField(blank=True, null=True)
    fullchain = LongTextField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    cloudflare_api_key = models.ForeignKey(CloudflareAPIKey, blank=True, null=True, on_delete=models.CASCADE, related_name='domains', help_text="Cloudflare API key used for DNS challenge")
    email = models.EmailField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate the expiration date if the certificate is provided
        if self.certificate:
            cert = x509.load_pem_x509_certificate(self.certificate.encode(), default_backend())
            self.expiration_date = cert.not_valid_after
        else:
            self.expiration_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.domain_name

