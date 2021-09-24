from django.urls import path

from . import views

app_name = 'screech'
urlpatterns = [
    path('public/', views.public, name='index'),
    path('public/store/', views.screech_public, name='store_public'),
    path('private/', views.private, name='private'),
    path('private/store/', views.screech_private, name='store_private')
]
