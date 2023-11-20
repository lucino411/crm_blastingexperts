from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.views.generic.edit import FormView
from django.shortcuts import reverse, render, get_object_or_404

from .models import Agent
from .forms import AgentModelForm, AddAgentForm
from organization.models import Organization
from option.mixins import OrganisorAndLoginRequiredMixin
from userprofile.models import CustomUser


class AgentListView(ListView):
    template_name = 'agent/agent_list.html'
    model = Organization
    context_object_name = 'organizations'

    def get_queryset(self):
        # Obtener el organizador actual (asumiendo que está disponible en la solicitud)
        current_organizer = self.request.user  # Reemplaza esto con la forma en que obtienes el organizador actual
        print(current_organizer)

        # Filtrar las organizaciones por el organizador actual
        queryset = Organization.objects.filter(created_by=current_organizer)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agents = CustomUser.objects.filter(organizations__in=self.object_list)
        context['agents'] = agents
        return context


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Agregar las organizaciones a las que pertenecen los agentes al contexto
    #     context['agents'] = Agent.objects.filter(organizations__in=context['organizaciones'])
    #     print(context['agents'])
    #     return context


class AgentCreateView(OrganisorAndLoginRequiredMixin, View):
    template_name = 'agent/agent_create.html'

    def get(self, request):
        # Obtener todos los agentes disponibles que no están ya en una organización
        available_agents = CustomUser.objects.filter(is_agent=True)

        print('availllllable')
        print(available_agents)

        # Obtener todas las organizaciones creadas por el organizador
        user_organizations = Organization.objects.filter(
            created_by=request.user)

        context = {
            'available_agents': available_agents,
            'user_organizations': user_organizations,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        # Obtener el ID del agente y la organización seleccionados del formulario
        agent_id = request.POST.get('agent_id')
        organization_id = request.POST.get('organization_id')

        if agent_id and organization_id:
            agent_user = get_object_or_404(CustomUser, id=agent_id, is_agent=True)
            organization = get_object_or_404(
                Organization, id=organization_id, created_by=request.user)
            # Verificar si el agente ya pertenece a la organización
            if not organization.members.filter(id=agent_user.id).exists():
                # Agregar el agente a la organización
                organization.members.add(agent_user)
                messages.success(
                    request, f"El agente {agent_user.username} se ha agregado a la organización {organization.name}.")
            else:
                messages.warning(
                    request, f"El agente {agent_user.username} ya pertenece a la organización {organization.name}.")
        else:
            messages.error(
                request, "Por favor, selecciona un agente y una organización.")

        return HttpResponseRedirect(reverse('agent:agent_create'))
