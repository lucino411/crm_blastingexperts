from django.urls import path
from .views import AgentListView

app_name = 'agent'

urlpatterns = [
    path('list/', AgentListView.as_view(), name='agent_list'),
    # Agrega otras URL según sea necesario
]
