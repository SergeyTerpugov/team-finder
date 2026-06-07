from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from constants import constants_projects as constant
from team_finder import utils as util
from projects.forms import ProjectForm
from projects.models import Project


def home_redirect(request):
    return redirect('projects:list')


def project_list_view(request):
    projects = Project.objects.select_related('owner').prefetch_related('participants').all().order_by('-created_at')
    page_obj = util.paginate(request, projects)
    return render(request, 'projects/project_list.html', {'projects': page_obj})


def project_detail_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:detail', project_id=project.pk)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': False
    })


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:detail', project_id=project.pk)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
        'project': project
    })


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    is_participant = project.participants.filter(pk=request.user.pk).exists()

    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({
        'status': 'ok',
        'participating': not is_participant
    })


@login_required
@require_POST
def complete_project(request, project_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Проект не найден'
            },
            status=HTTPStatus.NOT_FOUND
        )

    if project.owner != request.user:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Только автор может завершить проект'
            },
            status=HTTPStatus.FORBIDDEN
        )

    if project.status != constant.STATUS_OPEN:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Проект уже завершён'
            },
            status=HTTPStatus.BAD_REQUEST
        )

    project.status = constant.STATUS_CLOSED
    project.save()

    return JsonResponse({
        'status': 'ok',
        'project_status': constant.STATUS_CLOSED
    })
