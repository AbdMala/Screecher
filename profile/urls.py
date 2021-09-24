from django.urls import path

from . import views
from . import json

app_name = 'profile'
urlpatterns = [
    path('', views.profile, name='index'),
    path('upload/', views.upload_profile_pic, name='upload'),
    path('delete/', views.delete_profile_pic, name='delete'),
    path('change_username/', views.change_username, name='change_username'),
    path('companion/', views.companion, name='companion'),
    path('json/', json.toJson, name='json')
]
