from django.urls import path
from .views import OrganizationListView, OrganizationDetailView, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView

app_name = 'organization'

urlpatterns = [
    path('list/', OrganizationListView.as_view(), name='organization_list'),
    path('create/', OrganizationCreateView.as_view(), name='organization_create'),
    path('<int:pk>/', OrganizationDetailView.as_view(), name='organization_detail'),
    path('<int:pk>/update', OrganizationUpdateView.as_view(), name='organization_update'),
    path('<int:pk>/delete', OrganizationDeleteView.as_view(), name='organization_delete'),
]
