from django.contrib import admin
from .models import FriendRequest, Notification


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'is_accepted', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('is_accepted', 'created_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
