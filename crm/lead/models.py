from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _  # ayuda en traducciones

from choices.choices import *
from option.models import Title, Currency, ProductCategory, Provider, Country
from userprofile.models import CustomUser


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
    primary_email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=20, blank=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, null=True, blank=True)
    company = models.CharField(
        max_length=100, unique=False, blank=True)
    legal_nature = models.CharField(
        max_length=10, choices=LEGAL_NATURE_CHOICES, default='Private')
    website = models.URLField(blank=True)
    lead_source = models.CharField(
        max_length=100, choices=LEAD_SOURCE_CHOICES, blank=True)
    lead_status = models.CharField(
        max_length=100, choices=LEAD_STATUS_CHOICES, default='New')
    last_contacted_on = models.DateField(blank=True)
    last_contacted_via = models.CharField(
        max_length=20, choices=LAST_CONTACTED_VIA_CHOICES, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True)
    record_conversion_rate = models.FloatField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, blank=True)
    product_name = models.CharField(max_length=100, blank=True)
    product_website = models.URLField(blank=True)
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, blank=True)
    description = models.TextField(blank=False)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_leads', on_delete=models.SET_NULL, null=True, blank=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_leads', on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='last_modified_leads', on_delete=models.SET_NULL, null=True)
    is_closed = models.BooleanField(default=False)
    erased = models.BooleanField(default=False)
    pipeline = models.CharField(max_length=100, default='Standard')

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

        # if not self.assigned_to and not self.pk:
        #     try:
        #         default_assigned_to_instance = DefaultAssignedTo.objects.first()
        #         if default_assigned_to_instance:
        #             self.assigned_to = default_assigned_to_instance.user
        #         else:
        #             self.assigned_to = self.created_by
        #     except ObjectDoesNotExist:
        #         pass

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
