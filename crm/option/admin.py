from django.contrib import admin

from .models import Country, Currency, ProductCategory, Provider, Title


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    ordering = ['name']  # Reemplaza 'user' con el campo apropiado por el cual deseas ordenar alfabéticamente
    list_display = ('name', 'is_selected')  # Agrega el campo is_selected a la lista de exhibición
    search_fields = ('name',)

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    ordering = ['name']  # Reemplaza 'name' con el campo apropiado por el cual deseas ordenar alfabéticamente
    
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    ordering = ['name']  # Reemplaza 'name' con el campo apropiado por el cual deseas ordenar alfabéticamente

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    ordering = ['name']  # Reemplaza 'name' con el campo apropiado por el cual deseas ordenar alfabéticamente

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    ordering = ['name']  # Reemplaza 'name' con el campo apropiado por el cual deseas ordenar alfabéticamente


