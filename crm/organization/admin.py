from django.contrib import admin
from .models import Organization
from userprofile.models import CustomUser

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = CustomUser.objects.filter(is_organizator=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_active and request.user.is_superuser and request.user.is_organizator

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by == request.user:
            return True  # Permitir la edición si el usuario actual creó la organización
        return False

    # def has_delete_permission(self, request, obj=None):
    #     if obj is not None and obj.created_by == request.user:
    #         return True  # Permitir la eliminación si el usuario actual creó la organización
    #     return False  

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva organización
            # Establecer el organizador que crea la organización como el creador
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        # Ocultar el campo created_by y members
        return ('created_by', 'members')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_organizator:
            return qs.filter(created_by=request.user)
        return qs.none()  # Devolver un queryset vacío si el usuario no es un organizador
    








