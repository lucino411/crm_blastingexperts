from .models import Lead
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


from .forms import AddLeadFormForRegistered, AddLeadFormForAnonymous
from typing import Any
from .models import Lead, Country
from userprofile.models import CustomUser
from lead.models import DefaultCreatedBy, DefaultAssignedTo


''' 
/************
LIST LEADS
/************
'''

@login_required
def homeLead(request):
    context = {}
    context['titulo'] = 'Gestion de Leads'
    return render(request, 'leads/leads_list.html', context)


# Query de Leads de la base de datos enviada a JS como JSON para las Datatables JS
class LeadListView(ListView):
    model = Lead

    def get(self, request, *args, **kwargs):
        leads = self.get_queryset()
        leads_data = list(leads.values('id', 'first_name', 'last_name', 'primary_email',
                                       'country', 'created_time', 'modified_time', 'assigned_to_id', 'created_by_id'))
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

        return JsonResponse({'leads': leads_data})

'''
En Python, super() se utiliza para acceder y llamar a métodos definidos en la clase base. En el contexto de la clase LeadListView que estás creando, super().get_context_data(**kwargs) se refiere al método get_context_data de la clase base, en este caso, la clase ListView de Django. Estás llamando al método get_context_data de la clase base y pasándole cualquier argumento que se haya proporcionado a tu clase LeadListView.
Esto es útil porque te permite aprovechar la implementación existente de get_context_data en la clase base y extenderla según sea necesario. Al llamar a super().get_context_data(**kwargs), estás asegurándote de que cualquier lógica necesaria definida en la clase base se ejecute antes de tu propia lógica personalizada, lo que te permite agregar o modificar el contexto según sea necesario mientras mantienes el comportamiento básico de la clase base.

En el código proporcionado, context['leads'] = leads está asignando la variable leads al diccionario context con la clave 'leads'. En este caso, leads representa el queryset de todos los objetos Lead obtenidos de la base de datos.
Al definir context['leads'] = leads, estás pasando el queryset completo de objetos Lead a la plantilla, lo que te permite acceder a todos los campos y atributos de cada objeto Lead en el queryset dentro de la plantilla. No es necesario pasar explícitamente cada campo individual como parte de context para poder acceder a ellos en la plantilla.
Dentro de la plantilla, puedes acceder a los campos y atributos de cada objeto Lead en el queryset utilizando la sintaxis de plantilla de Django, como {{ lead.first_name }}, {{ lead.last_name }}, {{ lead.phone }}, etc., donde lead es cada objeto Lead en el queryset. Esto te permite mostrar o manipular los datos de cada objeto Lead directamente en la plantilla sin tener que pasar cada campo individualmente a través de context.
'''


''' 
/************
ADD LEAD
/************
'''

@user_passes_test(lambda u: u.is_active and (u.is_staff or u.is_superuser))
@login_required
def create_lead_registered(request):
    form = AddLeadFormForRegistered(request.POST)
    form.fields['country'].queryset = Country.objects.filter(is_selected=True)  # Aplicar el filtro en el formulario
    form.fields['assigned_to'].queryset = CustomUser.objects.filter(
        Q(is_staff=True, is_superuser=True) |
        Q(is_staff=True, is_superuser=False) |
        Q(is_staff=False, is_superuser=True)
    ).exclude(username='deleted')

    if request.method == 'POST':
        email = request.POST.get('primary_email')
        if Lead.objects.filter(primary_email=email).exists():
            messages.error(request, "This email already exists.")
        else:
            if form.is_valid():
                form.cleaned_data['created_by'] = request.user
                form.cleaned_data['last_modified_by'] = request.user
                Lead.objects.create(**form.cleaned_data)
                messages.success(request, "Lead was created")
                return redirect('leads:leads')
            else:
                messages.error(
                    request, "Invalid form data. Please check the entries and try again.")    
    context = {
        'form' : form
    }
    return render(request, 'leads/lead_create_authenticated.html', context)
    
   
'''
hemos utilizado form.cleaned_data para obtener un diccionario con los datos limpios y validados del formulario. Luego, hemos pasado ese diccionario directamente a create() utilizando el operador ** para desempaquetar los valores del diccionario como argumentos de la función create(). Esto nos permite crear el objeto Lead con todos los campos del formulario sin necesidad de agregarlos uno por uno.
'''

def create_lead_anonymous(request):
    form = AddLeadFormForAnonymous(request.POST)
    form.fields['country'].queryset = Country.objects.filter(
        is_selected=True)  # Aplicar el filtro en el formulario
    form.fields['assigned_to'].queryset = CustomUser.objects.filter(
        Q(is_staff=True, is_superuser=True) |
        Q(is_staff=True, is_superuser=False) |
        Q(is_staff=False, is_superuser=True)
    ).exclude(username='deleted')
    if request.method == 'POST':
        email = request.POST.get('primary_email')
        if Lead.objects.filter(primary_email=email).exists():
            messages.error(request, "This email already exists.")
        else:
            if form.is_valid():
                email = form.cleaned_data['primary_email']
                try:
                    Lead.objects.get(primary_email=email)
                    messages.error(request, "This email already exists.")
                except Lead.DoesNotExist:
                    if not request.user.is_authenticated:
                        if DefaultCreatedBy.objects.first():
                            form.cleaned_data['created_by'] = DefaultCreatedBy.objects.first(
                            ).user
                            form.cleaned_data['last_modified_by'] = DefaultCreatedBy.objects.first(
                            ).user
                        else:
                            form.cleaned_data['created_by'] = CustomUser.objects.first(
                            ).user
                            form.cleaned_data['last_modified_by'] = CustomUser.objects.first(
                            ).user

                        if DefaultAssignedTo.objects.first():
                            form.cleaned_data['assigned_to'] = DefaultAssignedTo.objects.first(
                            ).user
                        else:
                            form.cleaned_data['assigned_to'] = CustomUser.objects.first(
                            ).user

                Lead.objects.create(**form.cleaned_data)
                messages.success(request, "Lead was created")
                return redirect('leads:leads')
            else:
                messages.error(
                    request, "Invalid form data. Please check the entries and try again.")
    context = {
        'form': form
    }
    return render(request, 'leads/lead_create_anonymous.html', context)


''' 
/************
LEAD DETAIL
/************
'''

@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    context = {'lead': lead}
    return render(request, 'leads/lead_detail.html', context)


''' 
/************
LEAD UPDATE
/************
'''

@login_required
def leads_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = AddLeadFormForAnonymous(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead was updated")
            return redirect('leads:leads')
        else:
            messages.error(request, "Invalid form data. Please check the entries and try again.")            
    else:
        form = AddLeadFormForAnonymous(instance=lead)
    context = {
        'form': form,
    }

    return render(request, 'leads/leads_update.html', context)