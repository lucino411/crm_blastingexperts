from django.urls import path

from lead import views

app_name = 'leads'

urlpatterns = [
    path('list', views.homeLead, name='leads'),
    path('leads_json/', views.LeadListView.as_view(), name='leads_json'),
    path('create/', views.create_lead_registered, name='lead_create'),
    path('create_be/', views.create_lead_anonymous, name='lead_create_be'),
    path('<int:pk>/', views.leads_detail, name = 'lead_detail'),
    path('<int:pk>/update/', views.leads_update, name = 'lead_update'),
]