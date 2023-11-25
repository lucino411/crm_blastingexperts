from django.shortcuts import reverse
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView
from option.mixins import OrganisorAndLoginRequiredMixin
from .models import Organization
from .forms import OrganizationCreateModelForm


class OrganizationListView(OrganisorAndLoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization/organization_list.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_organizator'] = self.request.user.is_organizator
        return context
    

class OrganizationDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'organization/organization_detail.html'
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizer'] = self.object.created_by
        context['agents'] = self.object.members.filter(is_agent=True)
        return context
   
class OrganizationCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = 'organization/organization_create.html'
    form_class = OrganizationCreateModelForm

    def form_valid(self, form):
        organization = form.save(commit=False)
        # Establecer el organizador que crea la organización como el creador
        organization.created_by = self.request.user
        organization.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('organization:organization_list')
    
class OrganizationUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'organization/organization_update.html'
    fields = ['name', 'email']  # Agrega los campos que se pueden editar

    def get_queryset(self):
        # Filtra las organizaciones basadas en el usuario que las creó
        return Organization.objects.filter(created_by=self.request.user)
    
    def get_success_url(self):
        return reverse('organization:organization_detail', kwargs={"pk": self.get_object().id})

'''
self.get_object(): Obtiene el objeto de la organización que se acaba de actualizar.
.id: Accede al atributo id del objeto para obtener el identificador único de la organización.
Luego, reverse se utiliza para construir la URL utilizando el nombre de la vista 'organization:organization_detail' y proporcionando el argumento kwargs que incluye el identificador único (pk) de la organización actualizada.

La función reverse se utiliza para construir la URL basándose en el nombre de la vista y los argumentos proporcionados en kwargs. En este caso:

return reverse('organization:organization_detail', kwargs={"pk": self.get_object().id})
'organization:organization_detail': Es el nombre de la vista que se encuentra en la URLconf de la aplicación bajo el namespace 'organization'.
kwargs={"pk": self.get_object().id}: Aquí, le estás diciendo a Django que espere un argumento llamado "pk" en la URL y le proporcionas el valor del identificador (id) del objeto organización (self.get_object()).
Cuando esta URL se utiliza como destino para redirigir al usuario después de una actualización exitosa, el identificador (pk) se incluirá en la URL, y este valor estará disponible en la vista correspondiente para acceder a través de la variable pk. Por ejemplo, si la URL generada es algo como /organization/detail/1/, el valor 1 sería el pk y estaría disponible en la vista asociada para usarlo como sea necesario.
En resumen, después de que la organización se actualiza exitosamente, la aplicación redirige al usuario a la página de detalles de esa organización específica. Esto proporciona una mejor experiencia de usuario al mostrar la información actualizada después de la acción.

Django utiliza el patrón de URL definido en tu archivo urls.py para determinar cómo mapear las partes de la URL a parámetros que se pasan a las vistas. Si has definido una URL como /organization/1/detail/, Django esperará que haya un patrón de URL coincidente en tu archivo urls.py, algo así como:

path('organization/<int:pk>/detail/', OrganizationDetailView.as_view(), name='organization_detail')

En este caso, <int:pk> indica que esperamos un entero (el identificador) en esa posición de la URL y que se pasará como un parámetro llamado "pk" a la vista.

Si tu URL es /organization/detail/1/, el patrón de URL correspondiente debería ser algo como:

path('organization/detail/<int:pk>/', OrganizationDetailView.as_view(), name='organization_detail')

En ambos casos, el nombre del parámetro (<int:pk>) es importante, ya que se usa para extraer el valor de la URL y pasarlo a la vista.
'''

class OrganizationDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "organization/organization_delete.html"

    def get_success_url(self):
        return reverse("organization:organization_list")
    
    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(created_by=user)
