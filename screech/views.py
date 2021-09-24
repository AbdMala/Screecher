from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from screech.models import Screech


@login_required()
@require_GET
def public(request):
    screeches = Screech.objects.filter(private=False).order_by('-date')
    return render(request, 'screech/screech.html', context={'screeches': screeches, 'public': True})


@login_required()
@require_POST
def screech_public(request):
    content = request.POST.get('screech_area', '')
    if not content:
        messages.warning(request, 'Screech may not be empty')
        return redirect(reverse('screech:index'))

    Screech.objects.create(user=request.user, content=content, private=False)
    messages.info(request, 'Posted public Screech')
    return redirect(reverse('screech:index'))


@login_required()
@require_GET
def private(request):
    screeches = Screech.objects.filter(user=request.user, private=True).order_by('-date')
    return render(request, 'screech/screech.html', context={'screeches': screeches, 'public': False})


@login_required()
@require_POST
def screech_private(request):
    content = request.POST.get('screech_area', '')
    if not content:
        messages.warning(request, 'Screech may not be empty')
        return redirect(reverse('screech:private'))

    Screech.objects.create(user=request.user, content=content, private=True)
    messages.info(request, 'Posted private Screech')
    return redirect(reverse('screech:private'))
