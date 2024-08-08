from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_project, name='start_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
]
