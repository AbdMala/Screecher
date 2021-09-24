from re import search

from django.conf.global_settings import SESSION_COOKIE_AGE
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import reverse, redirect
from django.views.decorators.http import require_POST, require_http_methods

from profile.models import ProfilePicture
from screecher.utils import get_missing_migrations, migrations_applied, error_status


def _migrations_missing(request):
    missing_migrations = get_missing_migrations()
    if missing_migrations:
        messages.warning(request, f"Missing migrations! Please run \"python3 manage.py makemigrations {' '.join(missing_migrations)}\".")
        return True
    elif not migrations_applied():
        messages.warning(request, 'There are unapplied migrations! Please run "python3 manage.py migrate".')
        return True
    else:
        return False


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if _migrations_missing(request):
        return redirect(reverse('index'))

    if request.method == 'GET':
        if 'next' in request.GET:
            messages.warning(request, f"You must be logged in to access {request.GET.get('next')}")
            return redirect(f"{reverse('index')}?next={request.GET.get('next')}")
        return redirect(reverse('index'))
    else:
        username = request.POST.get('user', '')
        password = request.POST.get('pwd', '')
        timezone = request.POST.get('timezone')

        if not username or not password:
            messages.warning(request, 'Username/Password missing')
            return redirect(reverse('index'))

        try:
            username = User.objects.get(username__iexact=username).username
        except User.DoesNotExist:
            messages.warning(request, f"User '{username}' does not exist")
            return redirect(reverse('index'))

        user = authenticate(request=request, username=username, password=password)
        if user is None:
            messages.warning(request, f"Incorrect password for user '{username}'")
            return redirect(reverse('index'))
        else:
            login(request, user)
            messages.success(request, 'Login succeeded')
            response = redirect(request.POST.get('next', reverse('index')))
            if timezone is not None:
                response.set_cookie('timezone', timezone, expires=SESSION_COOKIE_AGE)
            return response


@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        response = redirect(reverse('index'))
        response.delete_cookie('timezone')
        messages.success(request, 'Logout succeeded')
        return response
    else:
        return error_status(401)


@require_POST
def signup_view(request):
    if _migrations_missing(request):
        return redirect(reverse('index'))

    username = request.POST.get('user', '')
    password = request.POST.get('pwd', '')
    password_verifier = request.POST.get('pwd_verifier', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    timezone = request.POST.get('timezone')

    if not (username and password and password_verifier and first_name and last_name and email):
        return error_status(400, 'Missing parameters')
    if not search(r"^\w+$", username):
        messages.warning(request, 'Illegal username: Username may only contain _ and alphanumeric characters')
        return redirect(reverse('index'))
    if password != password_verifier:
        messages.warning(request, 'Passwords do not match')
        return redirect(reverse('index'))

    try:
        user = User.objects.create_user(username=username.capitalize(), password=password, first_name=first_name,
                                        last_name=last_name, email=email)
    except IntegrityError:
        messages.warning(request, 'Username already taken')
        return redirect(reverse('index'))

    ProfilePicture.objects.create(user=user)

    login(request, user)
    messages.success(request, 'Registration succeeded')
    response = redirect(reverse('index'))
    if timezone is not None:
        response.set_cookie('timezone', timezone, expires=SESSION_COOKIE_AGE)
    return response
