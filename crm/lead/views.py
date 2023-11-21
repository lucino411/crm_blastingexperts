from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import reverse, render, redirect, get_object_or_404
from django.db.models import Q

from .models import Lead, Country
from userprofile.models import CustomUser
from organization.models import Organization
from .forms import AddLeadFormForRegistered, AddLeadFormForAnonymous
from lead.models import DefaultCreatedBy, DefaultAssignedTo

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
# class LeadListView(ListView):
#     model = Lead

    # def get_queryset(self):
        # Filtra los leads basados en el agente actualmente autenticado
        # return Lead.objects.filter(assigned_to=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     leads = self.get_queryset()
    #     leads_data = list(leads.values('id', 'first_name', 'last_name', 'primary_email',
    #                                    'country', 'created_time', 'modified_time', 'assigned_to_id', 'created_by_id'))
    #     country_names = {
    #         country.id: country.name for country in Country.objects.all()
    #     }
    #     user_names = {
    #         user.id: f"{user.first_name} {user.last_name}" for user in CustomUser.objects.all()
    #     }

    #     for lead in leads_data:
    #         lead['country'] = country_names.get(lead['country'])
    #         lead['assigned_to'] = user_names.get(lead['assigned_to_id'])
    #         lead['created_by'] = user_names.get(lead['created_by_id'])

    #     return JsonResponse({'leads': leads_data})


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
    

# class LeadListView(ListView):
#     model = Lead

    # def get_queryset(self):
        # Obten la organización del agente actualmente autenticado

        # Filtra los leads basados en la organización del agente
        # return Lead.objects.filter(organization=user_organization)

    # def get(self, request, *args, **kwargs):
    #     # leads = self.get_queryset()
    #     user_organization = Organization.objects.filter(members=self.request.user).first()
    #     # leads = self.get_queryset().filter(organization=user_organization, assigned_to=self.request.user)
    #     leads_data = list(leads.values('id', 'first_name', 'last_name', 'primary_email',
    #                                    'country', 'created_time', 'modified_time', 'assigned_to_id', 'created_by_id'))
    #     country_names = {
    #         country.id: country.name for country in Country.objects.all()
    #     }
    #     user_names = {
    #         user.id: f"{user.first_name} {user.last_name}" for user in CustomUser.objects.all()
    #     }

    #     for lead in leads_data:
    #         lead['country'] = country_names.get(lead['country'])
    #         lead['assigned_to'] = user_names.get(lead['assigned_to_id'])
    #         lead['created_by'] = user_names.get(lead['created_by_id'])
    #         lead['organization'] = user_organization.name  # Agrega el nombre de la organización


    #     return JsonResponse({'leads': leads_data})

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
