from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


from .forms import AddLeadFormForRegistered, AddLeadFormForUnregistered
from typing import Any
from .models import Lead, Country
from userprofile.models import CustomUser
from lead.models import DefaultCreatedBy, DefaultAssignedTo


@login_required
def homeLead(request):
    context = {}
    context['titulo'] = 'Gestion de Leads'
    return render(request, 'list_lead.html', context)

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
'''

'''
En el código proporcionado, context['leads'] = leads está asignando la variable leads al diccionario context con la clave 'leads'. En este caso, leads representa el queryset de todos los objetos Lead obtenidos de la base de datos.

Al definir context['leads'] = leads, estás pasando el queryset completo de objetos Lead a la plantilla, lo que te permite acceder a todos los campos y atributos de cada objeto Lead en el queryset dentro de la plantilla. No es necesario pasar explícitamente cada campo individual como parte de context para poder acceder a ellos en la plantilla.

Dentro de la plantilla, puedes acceder a los campos y atributos de cada objeto Lead en el queryset utilizando la sintaxis de plantilla de Django, como {{ lead.first_name }}, {{ lead.last_name }}, {{ lead.phone }}, etc., donde lead es cada objeto Lead en el queryset. Esto te permite mostrar o manipular los datos de cada objeto Lead directamente en la plantilla sin tener que pasar cada campo individualmente a través de context.
'''

'''
class LeadListView(ListView):
    model = Lead
    template_name = 'lead/lead_list.html'  # Reemplaza 'lead_list.html' con el nombre de tu plantilla
    context_object_name = 'leads'  # El nombre de la variable en el contexto de la plantilla

    def get_queryset(self):
        return Lead.objects.values('id', 'first_name', 'last_name', 'phone', 'primary_email', 'company', 'country', 'created_time', 'assigned_to')

class LeadListView(ListView):
    model = Lead
    template_name = 'gestionLeads.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        leads = Lead.objects.all()
        context['titulo'] = 'Gestion de Leads'
        context['leads'] = leads
        context['fields'] = ['id', 'first_name', 'last_name', 'phone', 'primary_email', 'company', 'country', 'created_time', 'assigned_to']
        return context

La diferencia entre usar el método get_queryset y get_context_data en una vista basada en clases de Django es el propósito para el que cada uno de estos métodos está diseñado.
get_queryset: Este método se utiliza para devolver un queryset de objetos que se van a mostrar en la plantilla. Es útil cuando deseas filtrar o ajustar la lista de objetos antes de pasarla a la plantilla para su renderización.
get_context_data: Este método se utiliza para añadir datos adicionales al contexto que se pasará a la plantilla. Puedes utilizar este método para incluir variables adicionales o realizar cálculos antes de pasar los datos a la plantilla.
En tu implementación, estás utilizando get_context_data para agregar un título adicional al contexto, lo que te permite acceder a la variable 'titulo' en tu plantilla 'gestionLeads.html'.
En resumen, mientras que get_queryset se utiliza principalmente para devolver el conjunto de objetos que se van a mostrar, get_context_data se utiliza para agregar cualquier dato adicional al contexto que se pasará a la plantilla. Puedes usar ambos métodos juntos para lograr la funcionalidad deseada en tus vistas basadas en clases.


En el método get_queryset, puedes realizar varias manipulaciones en el queryset antes de devolverlo. Algunas de las manipulaciones comunes que puedes realizar son:
Filtrado: Puedes filtrar los resultados según ciertos criterios utilizando filtros de queryset de Django, como filter, exclude, annotate, aggregate, entre otros.
Ordenamiento: Puedes ordenar los resultados en función de uno o más campos utilizando el método order_by.
Restricción: Puedes restringir la cantidad de resultados utilizando slice para obtener un rango específico de resultados o first y last para obtener el primer o último objeto del queryset.
Anotaciones y agregaciones: Puedes agregar anotaciones y agregaciones a tu queryset para realizar cálculos o resúmenes sobre los campos del modelo.
Combinación de consultas: Puedes combinar varios querysets utilizando operadores como | (OR) y & (AND) para realizar consultas más complejas.
Estas manipulaciones te permiten ajustar y filtrar los resultados del queryset antes de pasarlos a la plantilla para su renderización, lo que te da un control más granular sobre los datos que se muestran en tu vista.

get_context_data se utiliza principalmente para agregar datos adicionales al contexto que se pasará a la plantilla. Esto te permite pasar no solo los objetos del queryset del modelo, sino también cualquier otro dato adicional que necesites en la plantilla, como variables adicionales, listas, diccionarios u otros valores calculados.
Es una forma útil de ampliar el contexto que se pasa a la plantilla con datos específicos que pueden no estar directamente relacionados con el queryset del modelo. Esto proporciona flexibilidad en la presentación de datos y la lógica de la plantilla, permitiéndote personalizar la información que se muestra según las necesidades específicas de tu aplicación.
'''

@user_passes_test(lambda u: u.is_active and (u.is_staff or u.is_superuser))
@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadFormForRegistered(request.POST)
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
    else:
        form = AddLeadFormForRegistered()
        form.fields['country'].queryset = Country.objects.filter(
            is_selected=True)  # Aplicar el filtro en el formulario
    return render(request, 'add_lead_authenticated.html', {'form': form})

def add_lead_unauthenticated(request):
    if request.method == 'POST':
        form = AddLeadFormForUnregistered(request.POST)
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
    else:
        form = AddLeadFormForUnregistered()
        form.fields['country'].queryset = Country.objects.filter(
            is_selected=True)  # Aplicar el filtro en el formulario
    return render(request, 'add_lead_unauthenticated.html', {'form': form})


@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    # lead = get_object_or_404(Lead, created_by=request.user, pk=pk) # de esta forma solo el usuario que creo el lead puede modificarla
    # lead = Lead.objects.get(pk=pk)

    lead = Lead.objects.get(id=pk)  # Obtener el lead de la base de datos
    form = AddLeadFormForUnregistered(instance=lead)  # Pasar los datos del lead al formulario
    context = {'form': form}
    return render(request, 'leads_detail.html', context)


    # return render(request, 'leads_detail.html', {'lead': lead})
