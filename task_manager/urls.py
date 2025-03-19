from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_tasks, name='home'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('delete_all/', views.delete_all_tasks, name='delete_all_tasks'),
    path('edit/<int:id>/', views.edit_task, name='edit_task'),
    path('ai_complete/', views.ai_complete, name='ai_complete'),
] 