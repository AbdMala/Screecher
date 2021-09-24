import time

import pytz
from django.conf import settings
from django.shortcuts import render
from django.urls import set_urlconf
from django.utils import timezone
from django.utils.cache import patch_vary_headers
from pytz import UnknownTimeZoneError

from screecher.settings import DEBUG
from screecher.utils import error_status


class ErrorPageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 400 <= response.status_code < 500 or response.status_code >= 500 and not DEBUG:
            return render(request, 'error.html',
                          context={'status': response.status_code, 'reason': response.reason_phrase},
                          status=response.status_code)
        else:
            return response


class MultiHostMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            self.process_request(request)
        except ValueError as error:
            return error_status(404, str(error))
        else:
            response = self.get_response(request)
            return self.process_response(request, response)

    def process_request(self, request):
        request.META['LoadingStart'] = time.time()
        host = request.META['HTTP_HOST']
        sub_dom = host.split('.')[0]

        if sub_dom in settings.HOST_MIDDLEWARE_URLCONF_MAP:
            new_url_conf = settings.HOST_MIDDLEWARE_URLCONF_MAP[sub_dom]

            if new_url_conf.split('.')[0] in settings.APP_NAMES + ['screecher']:
                set_urlconf(new_url_conf)
                request.urlconf = new_url_conf
                request.META['MultiHost'] = new_url_conf
            else:
                raise ValueError(f"App does not exist: {new_url_conf.split('.')[0]}")
        else:
            raise ValueError(f"Subdomain is not defined: {sub_dom}")

    def process_response(self, request, response):
        if 'MultiHost' in request.META:
            response['MultiHost'] = request.META.get('MultiHost')

        if 'LoadingStart' in request.META:
            _loading_time = time.time() - int(request.META['LoadingStart'])
            response['LoadingTime'] = '%.2fs' % (_loading_time,)

        if getattr(request, 'urlconf', None):
            patch_vary_headers(response, ('Host',))
        return response


class TimezoneMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        zone = request.COOKIES.get('timezone')

        if zone is not None:
            try:
                timezone.activate(pytz.timezone(zone))
            except UnknownTimeZoneError:
                timezone.deactivate()
        else:
            timezone.deactivate()

        return self.get_response(request)
