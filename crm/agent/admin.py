from django.contrib import admin, messages
from .models import Agent
from userprofile.models import CustomUser
from organization.models import Organization


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(is_agent=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "organizations":
            kwargs["queryset"] = Organization.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def has_add_permission(self, request):
        if request.user.is_organizator and CustomUser.objects.filter(is_agent=True).exists() and Organization.objects.exists():
            return True
        return False  
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo agente
            obj.created_by = request.user  # Establecer el organizador que crea el agente como el creador
        super().save_model(request, obj, form, change)
        
# Ocultar el campo created_by en el admin para todos los usuarios
    def get_exclude(self, request, obj=None):
        return ('created_by',)
