from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Asegúrate de importar el modelo CustomUser desde userprofiles.models


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # ... Agrega tus propios fieldsets si es necesario ...
    )

admin.site.register(CustomUser, CustomUserAdmin)
