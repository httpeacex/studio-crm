from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path
from crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth.LoginView.as_view(template_name='crm/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('', views.clients, name='clients'),
    path('clients/new/', views.client_form, name='client-new'),
    path('clients/<int:pk>/', views.client_detail, name='client-detail'),
    path('clients/<int:pk>/edit/', views.client_form, name='client-edit'),
    path('clients/<int:pk>/archive/', views.client_archive, name='client-archive'),
]
