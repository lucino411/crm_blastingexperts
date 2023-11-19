from django.views.generic import ListView
from .models import Agent
from userprofile.models import CustomUser
from organization.models import Organization


class AgentListView(ListView):
    model = Agent
    template_name = 'agent/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        # Obtener el usuario actual
        user = self.request.user

        # Verificar si el usuario es un organizador
        if user.is_organizator:
            # Filtrar los agentes basados en el organizador que los creó
            return Agent.objects.filter(created_by=user)
        else:
            # Si el usuario no es un organizador, devolver un queryset vacío
            return Agent.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar las organizaciones a las que pertenecen los agentes al contexto
        context['organizations'] = Organization.objects.all()
        return context
