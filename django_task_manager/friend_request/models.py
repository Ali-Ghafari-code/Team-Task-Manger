from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from django_task_manager import settings

User = get_user_model()


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_accepted = models.BooleanField(default=False)


def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({'Accepted' if self.is_accepted else 'Pending'})"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

