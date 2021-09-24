from os.path import join

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template import Template, RequestContext
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .models import Sign


@login_required()
@require_GET
def overview(request):
    signs_objects = Sign.objects.all()
    signs = [el.data['id'] for el in signs_objects]
    return render(request, 'horoscope/overview.html', context={'signs': signs})


@login_required()
@require_GET
def sign_overview(request, sign_id):
    sign = Sign.objects.filter(data__id=sign_id).first()

    if sign is None:
        raise Http404

    context = RequestContext(request, {'sign': sign.data})

    back_url = (
        f"https://{request.META['HTTP_HOST']}" if 'HTTP_REFERER' not in request.META else request.META['HTTP_REFERER'])

    with open(join(settings.BASE_DIR, 'horoscope/templates/horoscope/sign.html')) as f:
        template = Template(f.read().replace('back_url', back_url))

    return HttpResponse(content=template.render(context))


@login_required()
@require_POST
def personal_sign(request):
    signs_objects = Sign.objects.count()
    sign_id = sum(ord(c) for c in request.user.get_full_name()) % signs_objects
    return redirect(reverse('horoscope:sign', kwargs={'sign_id': sign_id}))
