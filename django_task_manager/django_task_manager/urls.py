
from django.contrib import admin
from django.urls import path, include

import account.urls
import friend_request.urls
import home_module.urls
import taskmanager.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_module.urls)),
    path('projects/', include(taskmanager.urls)),
    path('', include(friend_request.urls)),
    path('user/', include(account.urls)),
]
