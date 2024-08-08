from django.contrib import admin

from account import models
from account.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active']


admin.site.register(models.User, UserAdmin)
