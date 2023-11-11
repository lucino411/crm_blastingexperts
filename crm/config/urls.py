from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('lead.urls', namespace='leads')),
    path('', include('dashboard.urls')),   
]

