from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import handler404


from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_home'),
    path('accounts/login/', views.login_user, name = 'login_home' ),
    path('logout/', views.logout_user, name = 'logout' ),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]

handler404 = 'dashboard.views.page_not_found404'
