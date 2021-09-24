from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from profile.models import ProfilePicture
from screecher.utils import error_status
from .models import FriendshipRequest, Friendship


@login_required
@require_GET
def friends(request):
    pending_requests = FriendshipRequest.objects.filter(requested=request.user)
    return render(request, 'friends/friends.html', context={'pending_requests': pending_requests})


@login_required
@require_GET
def requests(request):
    sent_requests = FriendshipRequest.objects.filter(requester=request.user)
    return render(request, 'friends/requests.html', context={'sent_requests': sent_requests})


@login_required
@require_POST
def remove_friend(request):
    friend = request.POST.get('friend', '')

    if not friend:
        return error_status(400, 'Missing parameter')

    try:
        requested = User.objects.get(username__iexact=friend)
    except User.DoesNotExist:
        return error_status(400, 'Request user does not exist')

    friendship = Friendship.objects.filter(
        Q(user1=request.user, user2=requested) | Q(user1=requested, user2=request.user))

    if not friendship.exists():
        return error_status(400, 'Request friendship does not exist')
    else:
        friendship.delete()
        messages.success(request, f"Successfully removed {friend} from your friends")
        return redirect(reverse('friends:index'))


def _friend_request(request, accept):
    new_friend = request.POST.get('new_friend', '')

    if not new_friend:
        return error_status(400, 'Missing parameter')

    try:
        requester = User.objects.get(username__iexact=new_friend)
    except User.DoesNotExist:
        return error_status(400, 'Request user does not exist')

    try:
        fsr = FriendshipRequest.objects.get(requester=requester, requested=request.user)
    except FriendshipRequest.DoesNotExist:
        return error_status(400, 'Request friendship does not exist')

    if accept:
        if Friendship.objects.filter(
                Q(user1=request.user, user2=requester) | Q(user1=requester, user2=request.user)).exists():
            return error_status(400, 'Friendship for these users is already established')
        else:
            Friendship.objects.create(user1=request.user, user2=requester)
            messages.success(request, 'Friend successfully added')
    else:
        messages.success(request, 'Friend request successfully declined')

    fsr.delete()
    return redirect(reverse('friends:index'))


@login_required
@require_POST
def accept_friend_request(request):
    return _friend_request(request, True)


@login_required
@require_POST
def decline_friend_request(request):
    return _friend_request(request, False)


@login_required
@require_POST
def add_friend(request):
    new_friend = request.POST.get('new_friend', '')
    message = request.POST.get('message', '')

    if not new_friend:
        return error_status(400, 'Missing parameter')

    try:
        requested = User.objects.get(username__iexact=new_friend)
    except User.DoesNotExist:
        messages.warning(request, f"User does not exist: {new_friend}")
        return redirect(reverse('friends:requests'))

    if requested == request.user:
        messages.warning(request, 'Do you not have any real friends? Adding yourself is pointless...')
        return redirect(reverse('friends:requests'))

    if Friendship.objects.filter(
            Q(user1=request.user, user2=requested) | Q(user1=requested, user2=request.user)).exists():
        messages.warning(request, f"You and {new_friend} are already friends")
        return redirect(reverse('friends:requests'))

    if FriendshipRequest.objects.filter(requester=request.user, requested=requested).exists():
        messages.warning(request, f"You have already sent a friend request to {new_friend}")
        return redirect(reverse('friends:requests'))
    else:
        FriendshipRequest.objects.create(requester=request.user, requested=requested, message=message)
        messages.success(request, f"Sent friend request to {new_friend}")
        return redirect(reverse('friends:requests'))


@login_required
@require_POST
def revoke_friend_request(request):
    requested_friend = request.POST.get('requested_friend', '')

    if not requested_friend:
        return error_status(400, 'Missing parameter')

    try:
        requested = User.objects.get(username__iexact=requested_friend)
    except User.DoesNotExist:
        return error_status(400, 'Request user does not exist')

    try:
        fsr = FriendshipRequest.objects.get(requester=request.user, requested=requested)
    except FriendshipRequest.DoesNotExist:
        return error_status(400, 'Requested friendship object does not exist')

    fsr.delete()
    messages.success(request, 'Friend request successfully revoked')
    return redirect(reverse('friends:requests'))


@login_required
@require_GET
def friend_script(request):
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))

    own_domain = request.META.get('HTTP_HOST')

    friend_list = []
    for f in friendships:
        if f.user1.username == request.user.username:
            friend_list.append(
                [f.user2.username, f.user2.get_full_name(), ProfilePicture.objects.get(user=f.user2).path])
        else:
            friend_list.append(
                [f.user1.username, f.user1.get_full_name(), ProfilePicture.objects.get(user=f.user1).path])

    return render(request, 'friends/friend_script.js',
                  context={'friends': friend_list, 'own_domain': own_domain},
                  content_type='application/x-javascript')
