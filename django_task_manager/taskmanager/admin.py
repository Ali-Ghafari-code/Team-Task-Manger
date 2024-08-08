from django.contrib import admin

# Register your models here.
from taskmanager.models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(ProjectMember)
class ProjectMember(admin.ModelAdmin):
    list_display = ('project', 'user')