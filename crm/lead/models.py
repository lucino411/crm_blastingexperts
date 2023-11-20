from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _  # ayuda en traducciones

from choices.choices import *
from option.models import Title, Currency, ProductCategory, Provider, Country
from organization.models import Organization
from userprofile.models import CustomUser

def get_sentinel_user():
    user, created = CustomUser.objects.get_or_create(username="deleted")
    if created:
        # Si se crea un nuevo usuario, establece los otros campos según sea necesario
        user.set_unusable_password()
        user.save()
    return user

class DefaultCreatedBy(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class DefaultAssignedTo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Lead(models.Model):
    salutation = models.CharField(
        max_length=5, choices=SALUTATION_CHOICES, blank=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    primary_email = models.EmailField(unique=True, blank=False, help_text="Please use the following format: <em>YYYY-MM-DD</em>."                                      )
    phone = models.CharField(max_length=20, blank=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, null=True, blank=True)
    company = models.CharField(
        max_length=100, unique=False, blank=True)
    legal_nature = models.CharField(
        max_length=10, choices=LEGAL_NATURE_CHOICES, default='PRIVATE')
    website = models.URLField(blank=True)
    lead_source = models.CharField(
        max_length=100, choices=LEAD_SOURCE_CHOICES, default='WEBSITE')
    lead_status = models.CharField(
        max_length=100, choices=LEAD_STATUS_CHOICES, default='NEW')
    last_contacted_on = models.DateField(blank=True, null=True)
    last_contacted_via = models.CharField(
        max_length=20, choices=LAST_CONTACTED_VIA_CHOICES, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True, null=True)
    record_conversion_rate = models.FloatField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True)
    product_website = models.URLField(blank=True)
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=False)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_leads', on_delete=models.SET(get_sentinel_user))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_leads', on_delete=models.SET(get_sentinel_user))
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='last_modified_leads', on_delete=models.SET(get_sentinel_user))
    organization = models.ForeignKey(
        Organization, related_name='leads', on_delete=models.SET_NULL, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    erased = models.BooleanField(default=False)
    pipeline = models.CharField(
        max_length=100, choices=PIPELINE_CHOICES, default='STANDARD')

    def save(self, *args, **kwargs):
        # Verifica si no existe created_by y si no hay una instancia previa en la base de datos
        if not self.created_by and not self.pk:
            default_user_instance = DefaultCreatedBy.objects.first()
            if default_user_instance:
                self.created_by = default_user_instance.user

        if not self.assigned_to and not self.pk:
            default_assigned_to_instance = DefaultAssignedTo.objects.first()
            if default_assigned_to_instance:
                self.assigned_to = default_assigned_to_instance.user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.country}"

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['created_time']),
            models.Index(fields=['country']),
            models.Index(fields=['product_category', 'provider']),
        ]
