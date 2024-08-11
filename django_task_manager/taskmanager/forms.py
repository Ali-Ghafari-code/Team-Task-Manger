from django import forms

from account.models import User
from .models import Project, Milestone, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'projectName',
                'placeholder': 'Enter project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'projectDescription',
                'rows': 3,
                'placeholder': 'Enter project description'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'projectStartDate',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'projectEndDate',
                'type': 'date'
            }),
        }
        labels = {
            'name': 'Project Name',
            'description': 'Project Description',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Assign To'
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'start_date', 'due_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter task description'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'name': 'Task Name',
            'description': 'Task Description',
            'start_date': 'Start Task Date',
            'due_date': 'End Task Date',
        }


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['name']
