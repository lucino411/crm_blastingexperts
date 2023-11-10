from django.urls import path

from . import views

urlpatterns = [
    path('leads/', views.homeLead, name='leads'),
    path('leads_list/', views.LeadListView.as_view(), name='leads_list'),
    path('lead_add/', views.create_lead_registered, name='lead_add'),
    path('lead_add_be/', views.create_lead_anonymous, name='lead_add_be'),
    path('lead_detail/<int:pk>/', views.leads_detail, name = 'lead_detail'),
]