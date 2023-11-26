from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Lead, Country, DefaultCreatedBy, DefaultAssignedTo
from userprofile.models import CustomUser
from organization.models import Organization
from .forms import AddLeadFormForRegistered, AddLeadFormForAnonymous

''' 
/************
LIST LEADS
/************
'''
class HomeLeadView(LoginRequiredMixin, TemplateView):
    template_name = 'leads/leads_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestion de Leads'
        return context
    
# Query de Leads de la base de datos enviada a JS como JSON para las Datatables JS
class LeadListView(ListView):
    model = Lead

    def get_queryset(self):
        # Obten la organización del agente actualmente autenticado
        user_organization = Organization.objects.filter(members=self.request.user).first()

        # Filtra los leads basados en la organización del agente
        return Lead.objects.filter(organization=user_organization)

    def get(self, request, *args, **kwargs):
        user_organization = Organization.objects.filter(members=self.request.user).first()
        leads = self.get_queryset()
        leads_data = list(leads.values('id', 'first_name', 'last_name', 'primary_email',
                                       'country', 'created_time', 'modified_time', 'assigned_to_id', 'created_by_id', 'organization'))
        country_names = {
            country.id: country.name for country in Country.objects.all()
        }
        user_names = {
            user.id: f"{user.first_name} {user.last_name}" for user in CustomUser.objects.all()
        }

        for lead in leads_data:
            lead['country'] = country_names.get(lead['country'])
            lead['assigned_to'] = user_names.get(lead['assigned_to_id'])
            lead['created_by'] = user_names.get(lead['created_by_id'])
            lead['organization'] = user_organization.name  # Agrega el nombre de la organización

        return JsonResponse({'leads': leads_data})
    
''' 
/************
LEAD DETAIL
/************
'''
class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()

''' 
/************
LEAD UPDATE
/************
'''
class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = AddLeadFormForAnonymous
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:leads_list")

''' 
/************
LEAD DELETE
/************
'''
class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:leads_list')

''' 
/************
CREATE LEAD
/************
'''
class LeadCreateRegisteredView(UserPassesTestMixin, LoginRequiredMixin, FormView):
    template_name = 'leads/lead_create_authenticated.html'
    form_class = AddLeadFormForRegistered

    def test_func(self):
        return self.request.user.is_active and (self.request.user.is_staff or self.request.user.is_superuser)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['country'].queryset = Country.objects.filter(
            is_selected=True)     
        user_organization = Organization.objects.filter(members=self.request.user).first()

        form.fields['assigned_to'].queryset = user_organization.members.filter(is_agent=True)     

        return form

    def form_valid(self, form):
        email = form.cleaned_data['primary_email']
        if Lead.objects.filter(primary_email=email).exists():
            messages.error(self.request, "This email already exists.")
            return render(self.request, self.template_name, {'form': form})
        else:
            form.instance.created_by = self.request.user
            form.instance.last_modified_by = self.request.user

            # Obtener la organización del agente que está creando el lead
            user_organization = Organization.objects.filter(members=self.request.user).first()

            # Asignar la organización al lead
            form.instance.organization = user_organization

            form.save()
            
            messages.success(self.request, "Lead was created")
            return redirect('leads:leads_list')

    def form_invalid(self, form):
        messages.error(
            self.request, "Invalid form data. Please check the entries and try again.")
        return render(self.request, self.template_name, {'form': form})


class LeadCreateAnonymousView(FormView):
    template_name = 'leads/lead_create_anonymous.html'
    form_class = AddLeadFormForAnonymous

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['country'].queryset = Country.objects.filter(
            is_selected=True)
        form.fields['assigned_to'].queryset = CustomUser.objects.filter(
            Q(is_staff=True, is_superuser=True) |
            Q(is_staff=True, is_superuser=False) |
            Q(is_staff=False, is_superuser=True)
        ).exclude(username='deleted')
 
        return form

    def form_valid(self, form):
        email = form.cleaned_data['primary_email']
        if Lead.objects.filter(primary_email=email).exists():
            messages.error(self.request, "This email already exists.")
            return render(self.request, self.template_name, {'form': form})
        else:
            if DefaultCreatedBy.objects.first():
                form.instance.created_by = DefaultCreatedBy.objects.first().user
                form.instance.last_modified_by = DefaultCreatedBy.objects.first(
                ).user
            else:
                form.instance.created_by = CustomUser.objects.first(
                ).user
                form.instance.last_modified_by = CustomUser.objects.first(
                ).user

            if DefaultAssignedTo.objects.first():
                form.instance.assigned_to = DefaultAssignedTo.objects.first(
                ).user
            else:
                form.instance.assigned_to = CustomUser.objects.first().user

            form.save()
            messages.success(self.request, "Lead was created")
            return redirect('leads:leads_list')

    def form_invalid(self, form):
        messages.error(
            self.request, "Invalid form data. Please check the entries and try again.")
        return render(self.request, self.template_name, {'form': form})


''' 
/********************************************
SELECT DefaultAssignedTo AND DefaultCreatedBy
/********************************************
'''
class HomeConfLeadView(LoginRequiredMixin, View):
    template_name = 'leads/leads_conf.html'

    def get(self, request, *args, **kwargs):
        # Obtener la organización actual del organizador
        current_organizer = self.request.user
        organization = get_object_or_404(
            Organization, created_by=current_organizer)
        agents = CustomUser.objects.filter(organizations__in=[organization])

        # Obtener el agente seleccionado como DefaultAssignedTo
        default_assigned_to = DefaultAssignedTo.objects.filter(
            user__organizations=organization).first()

        # Obtener el agente seleccionado como DefaultCreatedBy
        default_created_by = DefaultCreatedBy.objects.filter(
            user__organizations=organization).first()

        # Renderizar la plantilla con la información obtenida
        return render(request, self.template_name, {
            'organization': organization,
            'agents': agents,
            'default_assigned_to': default_assigned_to,
            'default_created_by': default_created_by,
        })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_organizator:
            created_by_id = request.POST.get('created_by')
            assigned_to_id = request.POST.get('assigned_to')
            organization = get_object_or_404(Organization, created_by=request.user)

            # Actualiza DefaultCreatedBy si se proporciona un nuevo valor
            if created_by_id:
                DefaultCreatedBy.objects.update_or_create(
                    defaults={'user_id': created_by_id},
                    organization=organization
                )

            # Actualiza DefaultAssignedTo si se proporciona un nuevo valor
            if assigned_to_id:
               DefaultAssignedTo.objects.update_or_create(
                    defaults={'user_id': assigned_to_id},
                    organization=organization
                )

            messages.success(request, "Agentes seleccionados correctamente.")
            return redirect('leads:leads_conf')
        else:
            return HttpResponseForbidden("Permission denied")
