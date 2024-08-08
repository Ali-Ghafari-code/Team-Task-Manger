from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from account.models import User
from .models import Project, ProjectMember
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
    recent_projects = Project.objects.filter(
        Q(manager=request.user) | Q(team=request.user)
    ).order_by('-start_date')[:5]

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

    if request.method == 'POST':
        friend_username = request.POST.get('newTeamMemberUsername')
        if friend_username:
            try:
                friend = User.objects.get(username=friend_username)
                if friend in request.user.friends.all():
                    # Check if the friend is already a member of the project
                    if not ProjectMember.objects.filter(project=project, user=friend).exists():
                        # Add the friend to the project team
                        project.team.add(friend)
                        # Create a ProjectMember entry
                        ProjectMember.objects.get_or_create(project=project, user=friend)
                        messages.success(request, f'{friend_username} has been added to the project.')
                    else:
                        messages.info(request, f'{friend_username} is already a member of the project.')
                else:
                    messages.error(request, f'{friend_username} is not your friend.')
            except User.DoesNotExist:
                messages.error(request, f'User {friend_username} does not exist.')

        return redirect('project_detail', project_id=project.id)

    project_members = project.members.all()

    context = {
        'project': project,
        'progress': progress,
        'milestones': milestones,
        'form': form,
        'project_members': project_members,
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
