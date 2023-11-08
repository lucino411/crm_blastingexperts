from django.apps import AppConfig


class LeadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lead'


class LeadConfig(AppConfig):
    name = 'lead'

    def ready(self):
        import lead.signals  # Importa el archivo de señales
