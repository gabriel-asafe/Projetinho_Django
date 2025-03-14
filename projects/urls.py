from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('delete/<int:pk>/', views.project_delete, name='project_delete'),
    path('detail/<int:pk>/', views.project_detail, name='project_detail'),
    path('manage-members/<int:pk>/', views.project_manage_members, name='project_manage_members'),  # Nova rota
]