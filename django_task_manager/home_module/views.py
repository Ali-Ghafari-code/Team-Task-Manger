from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from taskmanager.models import Project


@login_required
def home_view(request):
    today = date.today()
    active_projects = Project.objects.filter(end_date__gte=today)
    past_projects = Project.objects.filter(end_date__lt=today)

    context = {
        'active_projects': active_projects,
        'past_projects': past_projects,
    }

    return render(request, 'home_module/index_page.html', context)


def site_header_partial(request):
    return render(request, 'shared/site_header_partial.html', {})


def site_footer_partial(request):
    return render(request, 'shared/site_footer_partial.html', {})
