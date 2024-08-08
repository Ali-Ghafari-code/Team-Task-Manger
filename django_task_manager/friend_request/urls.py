from django.urls import path
from . import views

urlpatterns = [
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('manage_friend_request/<int:request_id>/<str:action>/', views.manage_friend_request, name='manage_friend_request'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),

]
