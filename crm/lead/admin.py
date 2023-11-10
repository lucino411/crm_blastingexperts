from django.contrib import admin
from django.db.models import Q

from .models import Lead, DefaultCreatedBy, DefaultAssignedTo
from option.models import Country
from userprofile.models import CustomUser


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'country', 'created_time', 'modified_time']
    exclude = ['created_by', 'created_time', 'modified_time',
               'last_modified_by', 'is_closed', 'erased', 'pipeline']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["queryset"] = Country.objects.filter(is_selected=True)
        elif db_field.name == "assigned_to" or db_field.name == "created_by":
            kwargs["queryset"] = CustomUser.objects.filter(
                Q(is_staff=True, is_superuser=True) |
                Q(is_staff=True, is_superuser=False) |
                Q(is_staff=False, is_superuser=True)
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:  # Solo se aplica al crear un nuevo Lead
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)


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