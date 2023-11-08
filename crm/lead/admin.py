from django.contrib import admin

from .models import Lead, DefaultCreatedBy, DefaultAssignedTo
from option.models import Country
from userprofile.models import CustomUser

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'country', 'created_time', 'modified_time']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == "country":
                kwargs["queryset"] = Country.objects.filter(is_selected=True)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(DefaultCreatedBy)
class DefaultCreatedByAdmin(admin.ModelAdmin):
    ordering = ['user']  
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(is_active=True, is_superuser=True) | CustomUser.objects.filter(is_active=True, is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(DefaultAssignedTo)
class DefaultAssignedToAdmin(admin.ModelAdmin):
    ordering = ['user']  
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(is_active=True, is_superuser=True) | CustomUser.objects.filter(is_active=True, is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)