from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm, MilestoneForm


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
    recent_projects = Project.objects.filter(manager=request.user).order_by('-start_date')[:5]

    return render(request, 'projects/projects.html', {
        'form': form,
        'recent_projects': recent_projects,
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    progress = project.calculate_progress()
    milestones = project.milestones.all()
    form = MilestoneForm()

    context = {
        'project': project,
        'progress': progress,
        'milestones': milestones,
        'form': form,
    }
    return render(request, 'projects/project.html', context)


def manage_milestones(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.save()
            return redirect('project_detail', project_id=project.id)

    else:
        form = MilestoneForm()

    return render(request, 'projects/manage_milestones.html', {
        'form': form,
        'project': project,
    })
