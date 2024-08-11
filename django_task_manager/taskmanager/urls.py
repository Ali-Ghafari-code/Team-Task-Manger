from django.urls import path
from . import views


urlpatterns = [
    path('', views.start_project, name='start_project'),
    path('project/<int:project_id>/milestones/', views.manage_milestones, name='manage_milestones'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/add_task/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),

]
