import json
from http import HTTPStatus

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from constants import constants_teamfinder as t_constant
from team_finder import utils as util
from users.forms import ChangePasswordFormUser, EditFormUser, LoginFormUser, RegistrationFormUser
from users.models import Skill

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('projects:list')
    form = RegistrationFormUser(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('projects:list')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:list')

    form = LoginFormUser(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('projects:list')

        form.add_error(None, 'Неверный email или пароль')

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:list')


def user_detail_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile_view(request):
    form = EditFormUser(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    form = ChangePasswordFormUser(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        login(request, request.user)
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/change_password.html', {'form': form})


def users_list_view(request):
    users = User.objects.all()
    active_skill = request.GET.get('skill', '')

    if active_skill:
        users = users.filter(skills__name=active_skill).distinct()

    all_skills = Skill.objects.all().order_by('name')
    page_obj = util.paginate(request, users)
    context = {
        'participants': page_obj,
        'all_skills': all_skills,
        'active_skill': active_skill,
    }
    return render(request, 'users/participants.html', context)


@require_GET
def skills_autocomplete(request):
    query = request.GET.get('q', '')

    if query:
        skills = Skill.objects.filter(
            name__istartswith=query
        ).order_by('name')[:t_constant.SKILLS_AUTOCOMPLETE_LIMIT]
    else:
        skills = Skill.objects.none()

    skills_data = []
    for skill in skills:
        skills_data.append({
            'id': skill.id,
            'name': skill.name
        })

    return JsonResponse(skills_data, safe=False)


@login_required
@require_POST
def skills_add(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    if user is None:
        return JsonResponse(
            {'error': 'Пользователь не найден'},
            status=HTTPStatus.NOT_FOUND
        )

    if user != request.user:
        return JsonResponse(
            {'error': 'Нельзя редактировать чужой профиль'},
            status=HTTPStatus.FORBIDDEN
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Неверный формат данных'},
            status=HTTPStatus.BAD_REQUEST
        )

    skill_id = data.get('skill_id')
    name = data.get('name')

    created = False
    added = False

    if skill_id:
        skill = Skill.objects.filter(pk=skill_id).first()
        if skill is None:
            return JsonResponse(
                {'error': 'Навык не найден'},
                status=HTTPStatus.NOT_FOUND
            )

        if not user.skills.filter(pk=skill.pk).exists():
            user.skills.add(skill)
            added = True

    elif name:
        skill, created = Skill.objects.get_or_create(name=name.strip())

        if not user.skills.filter(pk=skill.pk).exists():
            user.skills.add(skill)
            added = True

    else:
        return JsonResponse(
            {'error': 'Нужно указать skill_id или name'},
            status=HTTPStatus.BAD_REQUEST
        )

    return JsonResponse({
        'skill_id': skill.id,
        'name': skill.name,
        'created': created,
        'added': added
    })


@login_required
@require_POST
def skills_remove(request, user_id, skill_id):
    user = User.objects.filter(pk=user_id).first()
    if user is None:
        return JsonResponse(
            {'error': 'Пользователь не найден'},
            status=HTTPStatus.NOT_FOUND
        )

    if user != request.user:
        return JsonResponse(
            {'error': 'Нельзя редактировать чужой профиль'},
            status=HTTPStatus.FORBIDDEN
        )
    skill = Skill.objects.filter(pk=skill_id).first()
    if skill is None:
        return JsonResponse(
            {'error': 'Навык не найден'},
            status=HTTPStatus.NOT_FOUND
        )
    if user.skills.filter(pk=skill.pk).exists():
        user.skills.remove(skill)
        return JsonResponse({'status': 'ok'})

    return JsonResponse(
        {'error': 'У пользователя нет такого навыка'},
        status=HTTPStatus.BAD_REQUEST
    )
