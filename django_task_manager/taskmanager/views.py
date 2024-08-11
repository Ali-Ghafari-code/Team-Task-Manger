from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from account.models import User
from friend_request.models import Notification
from .models import Project, ProjectMember, Task
from .forms import ProjectForm, MilestoneForm, TaskForm


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
    tasks = project.tasks.all()
    form = MilestoneForm()

    task_form = TaskForm()

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
        'task_form': task_form,
        'project_members': project_members,
        'tasks': tasks
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


def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    assigned_user = None
    if 'assigned_to' in request.GET:
        assigned_user = get_object_or_404(User, id=request.GET['assigned_to'])

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.project = project
            task.save()
            notification_message = f'You have been assigned a new task in the project "{project.name}".'
            Notification.objects.create(user=task.assigned_to, message=notification_message)

            messages.success(request, 'Task added successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        task_form = TaskForm(initial={'assigned_to': assigned_user} if assigned_user else None)

    return render(request, 'projects/project.html', {'task_form': task_form, 'project': project})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    # Check if the user is the task creator or project manager
    if request.user != task.assigned_to and request.user != project.manager:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task has been deleted successfully.')
        return redirect('project_detail', project_id=project.id)

    return redirect('project_detail', project_id=project.id)


@login_required
def tasks_view(request):
    tasks = Task.objects.all()

    incomplete_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)

    context = {
        'incomplete_tasks': incomplete_tasks,
        'completed_tasks': completed_tasks
    }

    return render(request, 'tasks/tasks.html', context)


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if the user is allowed to complete the task
    if request.user != task.assigned_to and request.user != task.project.manager:
        messages.error(request, 'You do not have permission to complete this task.')
        return redirect('tasks_view')

    if request.method == 'POST':
        task.completed = True
        task.save()
        messages.success(request, 'Task marked as complete.')
        return redirect('tasks_view')


@login_required
def reopen_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if the user is allowed to reopen the task
    if request.user != task.assigned_to and request.user != task.project.manager:
        messages.error(request, 'You do not have permission to reopen this task.')
        return redirect('tasks_view')

    if request.method == 'POST':
        task.completed = False
        task.save()
        messages.success(request, 'Task has been reopened.')
        return redirect('tasks_view')