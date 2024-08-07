from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects')
    start_date = models.DateField()
    end_date = models.DateField()
    team = models.ManyToManyField(User, related_name='projects', through='ProjectMembership')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_joined = models.DateField(default=timezone.now)
    role = models.CharField(max_length=255, choices=[('Manager', 'Manager'), ('Member', 'Member')])

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
