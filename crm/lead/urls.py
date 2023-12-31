from django.urls import path

from .views import HomeLeadView, LeadListView, LeadDetailView, LeadUpdateView, LeadDeleteView, LeadCreateRegisteredView, LeadCreateAnonymousView


app_name = 'leads'

urlpatterns = [
    path('list/', HomeLeadView.as_view(), name='leads_list'),
    path('create/', LeadCreateRegisteredView.as_view(), name='lead_create'),
    path('create_be/', LeadCreateAnonymousView.as_view(), name='lead_create_be'),
    path('leads_json/', LeadListView.as_view(), name='leads_json'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead_detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead_update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead_delete'),
]