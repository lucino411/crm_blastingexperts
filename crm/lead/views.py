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

# @login_required
class LeadListView(ListView):
    model = Lead

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        leads = self.get_queryset()
        leads_data = list(leads.values('id', 'first_name', 'last_name', 'primary_email',
                          'country', 'created_time', 'modified_time', 'assigned_to_id', 'created_by_id'))
        country_names = {
            country.id: country.name for country in Country.objects.all()}
        user_names = {
            user.id: f"{user.first_name} {user.last_name}" for user in CustomUser.objects.all()}

        for lead in leads_data:
            lead['country'] = country_names.get(lead['country'])
            lead['assigned_to'] = user_names.get(lead['assigned_to_id'])
            lead['created_by'] = user_names.get(lead['created_by_id'])

        context['leads'] = leads_data
        return context

    def render_to_response(self, context, **response_kwargs):
        leads = context['leads']
        return JsonResponse({'leads': leads}, safe=False)


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
        if form.is_valid():
            new_lead = form.save(commit=False)
            new_lead.created_by = request.user
            new_lead.last_modified_by = request.user
            new_lead.save()
            messages.success(request, "Lead was created")
            return redirect('leads')
        else:
            messages.error(
                request, "Invalid form data. Please check the entries and try again.")
    
    context = {
        'form' : form
    }
    return render(request, 'leads/lead_create_authenticated.html', context)
    
    
'''
El argumento commit=False en form.save(commit=False) en Django te permite crear una instancia del modelo sin guardarla inmediatamente en la base de datos. Esto es útil cuando necesitas realizar alguna manipulación adicional en la instancia antes de guardarla definitivamente.
Cuando utilizas commit=False, se crea una instancia del modelo, pero no se realiza la operación de guardar en la base de datos. Esto te da la oportunidad de realizar cambios adicionales en la instancia antes de guardarla. Luego, puedes llamar a save() en la instancia manualmente para persistirla en la base de datos.
En el caso de tu vista add_lead, esto se utiliza para asignar valores a los campos created_by y last_modified_by antes de guardar el objeto en la base de datos.

'''

def create_lead_anonymous(request):
    form = AddLeadFormForAnonymous(request.POST)
    form.fields['country'].queryset = Country.objects.filter(is_selected=True)  # Aplicar el filtro en el formulario
    form.fields['assigned_to'].queryset = CustomUser.objects.filter(
        Q(is_staff=True, is_superuser=True) |
        Q(is_staff=True, is_superuser=False) |
        Q(is_staff=False, is_superuser=True)
    ).exclude(username='deleted')
    if request.method == 'POST':
        if form.is_valid():
            new_lead = form.save(commit=False)
            if not request.user.is_authenticated:
                default_create_user_instance = DefaultCreatedBy.objects.first()
                default_assigned_to_user_instance = DefaultAssignedTo.objects.first()
                if default_create_user_instance:
                    new_lead.created_by = default_create_user_instance.user
                    new_lead.last_modified_by = default_create_user_instance.user
                else:
                    first_custom_user = CustomUser.objects.first()
                    new_lead.created_by = first_custom_user
                    new_lead.last_modified_by = first_custom_user

                if default_assigned_to_user_instance:
                    new_lead.assigned_to = default_assigned_to_user_instance.user
                else:
                    first_custom_user = CustomUser.objects.first()
                    new_lead.assigned_to = first_custom_user
            else:
                new_lead.created_by = request.user
                new_lead.last_modified_by = request.user
                new_lead.assigned_to = DefaultAssignedTo.objects.first().user
            new_lead.save()
            messages.success(request, "Lead was created")
            return redirect('leads')
        else:
            messages.error(
                request, "Invalid form data. Please check the entries and try again.")
    context = {
        'form': form
    }
    return render(request, 'leads/lead_create_anonymous.html', context)


@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    # lead = get_object_or_404(Lead, created_by=request.user, pk=pk) # de esta forma solo el usuario que creo el lead puede modificarla
    # lead = Lead.objects.get(pk=pk)

    lead = Lead.objects.get(id=pk)  # Obtener el lead de la base de datos
    # form = AddLeadFormForUnregistered(instance=lead)  # Pasar los datos del lead al formulario
    # context = {'form': form}
    context = {'lead': lead}
    return render(request, 'leads/lead_detail.html', context)
