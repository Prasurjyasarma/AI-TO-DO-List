"""
URL configuration for curd_opp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.view_tasks,name='home'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:id>',views.delete_task,name="delete_task"),
    path('delete_all/',views.delete_all_tasks,name="delete_all_tasks"),
    path('edit/<int:id>',views.edit_task,name="edit_task"),
    path('generate-description/', views.generate_description, name='generate_description'),
    
    
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/',views.logout_page,name="logout"),
    
    path('history/',views.history_tasks,name="history_tasks")
    
]
