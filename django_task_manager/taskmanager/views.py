from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


@login_required
def start_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
        return render(request, 'projects/projects.html', {'form': form})
    return render(request, 'projects/projects.html', {'form': form})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    progress = project.calculate_progress()

    context = {
        'project': project,
        'progress': progress,
    }
    return render(request, 'projects/project.html', context)
