from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
import secrets
from message.models import Message
from screecher.utils import error_status


@login_required()
@require_GET
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'message/inbox.html', {'received_messages': received_messages})


@require_http_methods(['GET', 'POST'])
@login_required()
def outbox(request):
    if request.method == 'GET':
        sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
        return render(request, 'message/outbox.html', {'sent_messages': sent_messages})
    else:

        try:
            message_id = int(request.POST.get('id'))
        except (ValueError, TypeError):
            return error_status(400, 'Missing/malformed parameter')
        try:
            msg = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return error_status(400, 'Requested message does not exist')
        text = '\n' * 3 + \
               f"At {str(msg.timestamp).partition('.')[0]} {msg.sender.get_full_name()} " \
               f"@{msg.sender.username} wrote:\n{msg.content}"
        tokens = "jdljfgljdfg"
        reply = {'receiver': msg.sender, 'text': text, 'tokens': tokens}  #
        sent_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
        return render(request, 'message/outbox.html', {'sent_messages': sent_messages, 'reply': reply})


@login_required()
@require_POST
def store_message(request):
    receiver = request.POST.get('receiver', '')
    content = request.POST.get('content', '')
    tokens = request.POST.get('tokens', '')
    if not receiver or not content or not tokens:
        return error_status(400, 'Missing parameter')

    try:
        receiver = User.objects.get(username__iexact=receiver)
    except User.DoesNotExist:
        messages.warning(request, f"User does not exist: {receiver}")
        return redirect(reverse('message:outbox'))

    Message.objects.create(sender=request.user, receiver=receiver, content=content)
    messages.success(request, 'Message successfully sent')
    return redirect(reverse('message:outbox'))


@login_required()
@require_POST
def delete_message(request):
    try:
        message_id = int(request.POST.get('id'))
    except (ValueError, TypeError):
        return error_status(400, 'Missing/malformed parameter')
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return error_status(400, 'Requested message does not exist')

    if message.sender != request.user:
        return error_status(400, 'Illegal delete request user')

    message.delete()
    messages.success(request, 'Message successfully deleted')
    return redirect(reverse('message:outbox'))


@login_required()
@require_POST
def mark_as_read(request):
    try:
        message_id = int(request.POST.get('id'))
    except (ValueError, TypeError):
        return error_status(400, 'Missing/malformed parameter')
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return error_status(400, 'Requested message does not exist')

    message.read = True
    message.save()
    messages.success(request, 'Message successfully marked as read')
    return redirect(reverse('message:index'))


@login_required()
@require_POST
def ignore_message(request):
    try:
        message_id = int(request.POST.get('id'))
    except (ValueError, TypeError):
        return error_status(400, 'Missing/malformed parameter')
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return error_status(400, 'Requested message does not exist')

    message.ignored = True
    message.save()
    messages.success(request, 'Message successfully removed')
    return redirect(reverse('message:index'))
