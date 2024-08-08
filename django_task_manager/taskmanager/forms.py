from django import forms
from .models import Project, Milestone


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


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['name']