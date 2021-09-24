from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic import RedirectView

from screecher.settings import STATIC_URL
from . import views

app_name = 'analytics'
urlpatterns = [
    path('', views.analytics, name='index'),
    path('favicon.ico', RedirectView.as_view(url=f"{STATIC_URL}img/screecher-ico.png", permanent=True))
]

# register static files base
urlpatterns += staticfiles_urlpatterns()