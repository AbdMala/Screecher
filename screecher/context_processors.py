from collections import defaultdict

from django.conf import settings

from profile.models import ProfilePicture


def app_names(request):
    return {'APPS': sorted([app for app in settings.APP_NAMES if app != 'accounts' and app != 'analytics'])}


def profile_pictures(request):
    profile_pics = defaultdict(lambda: '/static/profile/img/default.png')
    try:
        for profile_picture in ProfilePicture.objects.all():
            profile_pics[profile_picture.user_id] = profile_picture.path
    except:
        pass
    return {'PROFILE_PICTURES': profile_pics}
