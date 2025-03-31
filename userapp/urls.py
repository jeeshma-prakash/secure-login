from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name = 'login'),
    path('register/', views.register, name ='register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]