
from django.contrib import admin
from django.urls import path, include

import account.urls
import home_module.urls
import taskmanager.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_module.urls)),
    path('user/', include(account.urls))
]
