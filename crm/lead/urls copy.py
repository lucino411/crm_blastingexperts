from django.urls import path

from .views import HomeLeadView, LeadListView


app_name = 'leads'

urlpatterns = [
    # path('list', views.homeLead, name='leads'),
    path('list/', HomeLeadView.as_view(), name='leads'),
    path('leads_json/', LeadListView.as_view(), name='leads_json'),
    # path('create/', views.create_lead_registered, name='lead_create'),
    # path('create_be/', views.create_lead_anonymous, name='lead_create_be'),
    # path('<int:pk>/', views.lead_detail, name = 'lead_detail'),
    # path('<int:pk>/update/', views.lead_update, name = 'lead_update'),
    # path('<int:pk>/delete/', views.lead_delete, name = 'lead_delete'),
]