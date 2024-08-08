from datetime import date
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from account.models import User
from taskmanager.models import Project
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date


@login_required
def home_view(request):
    today = date.today()
    user = request.user

    active_projects = Project.objects.filter(
        (Q(manager=user) | Q(team=user)),
        end_date__gte=today
    ).distinct()

    past_projects = Project.objects.filter(
        (Q(manager=user) | Q(team=user)),
        end_date__lt=today
    ).distinct()
    context = {
        'active_projects': active_projects,
        'past_projects': past_projects,
    }

    return render(request, 'home_module/index_page.html', context)


def notification(request):
    notifications = request.user.notifications.filter(is_read=False)
    friends = request.user.friends.all()

    context = {
        'notifications': notifications,
        'friends': friends
    }

    return render(request, 'shared/notification.html', context)


def site_header_partial(request):
    return render(request, 'shared/site_header_partial.html', {})


def site_footer_partial(request):
    return render(request, 'shared/site_footer_partial.html', {})
