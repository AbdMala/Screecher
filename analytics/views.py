import json
import random
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from screech.models import Screech
from screecher.settings import SESSION_COOKIE_DOMAIN
from screecher.utils import error_status


def is_allowed_origin(http_origin, http_host):
    if http_origin:
        # get hostname part of http_origin
        origin_hostname = urlparse(http_origin).hostname

        # allow www.teamX.screecher.de access
        if origin_hostname == SESSION_COOKIE_DOMAIN and f"analytics.{origin_hostname}" == http_host:
            return True

        # allow access if proxy nullifies the header for privacy reasons
        if http_origin == 'null':
            return True
    return False


@require_http_methods(['OPTIONS', 'GET'])
def analytics(request):
    if request.method == 'OPTIONS':
        response = HttpResponse(status=200, content='Preflight')
        if is_allowed_origin(request.META.get('HTTP_ORIGIN'), request.META.get('HTTP_HOST')):
            response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        return response

    if request.user.is_authenticated:
        screech_num = Screech.objects.count()
        screech_num_user = Screech.objects.filter(user=request.user).count()
        screech_num_public = Screech.objects.filter(user=request.user, private=False).count()
        screech_num_private = Screech.objects.filter(user=request.user, private=True).count()
        screech_percentage = round((screech_num_user / screech_num) * 100, 2) if screech_num != 0 else 0.0
        screech_counts = [x["id__count"] for x in Screech.objects.values("user").annotate(Count("id"))]
        data = {
            'screech_num': screech_num,
            'screech_percentage': f"{screech_percentage}%",
            'screech_num_user': screech_num_user,
            'screech_user_ratio': f"{screech_num_public}:{screech_num_private}",
            'screech_num_max': max(screech_counts) if screech_counts else 0,
            'click_num': random.randint(50, 100),
            'click_user': random.choice(User.objects.all()).username,
            'lucky_number': ''.join(str(ord(c)) for c in request.user.first_name)
        }
        response = HttpResponse(json.dumps(data))
        if is_allowed_origin(request.META.get('HTTP_ORIGIN'), request.META.get('HTTP_HOST')):
            response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
            response['Access-Control-Allow-Credentials'] = 'true'
        return response
    else:
        return error_status(401)
