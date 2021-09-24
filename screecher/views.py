from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from screecher.settings import INSTALLED_APPS, SESSION_COOKIE_DOMAIN, SESSION_COOKIE_SAMESITE, MIDDLEWARE
from screecher.utils import get_missing_migrations, migrations_applied


@require_GET
def index(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'landing.html')


@require_GET
def version(_):
    return JsonResponse({
        'migrations': not(get_missing_migrations()) and migrations_applied(),
        'INSTALLED_APPS': INSTALLED_APPS,
        'MIDDLEWARE': MIDDLEWARE,
        'SESSION_COOKIE_DOMAIN': SESSION_COOKIE_DOMAIN,
        'SESSION_COOKIE_SAMESITE': SESSION_COOKIE_SAMESITE
    })
