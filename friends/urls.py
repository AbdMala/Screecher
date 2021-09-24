from django.urls import path

from . import views

app_name = 'friends'
urlpatterns = [
    path('', views.friends, name='index'),
    path('requests/', views.requests, name='requests'),
    path('remove/', views.remove_friend, name='remove_friend'),
    path('accept/', views.accept_friend_request, name='accept_friend'),
    path('decline/', views.decline_friend_request, name='decline_friend'),
    path('add/', views.add_friend, name='add_friend'),
    path('revoke/', views.revoke_friend_request, name='revoke_friend'),
    path('friendscript/', views.friend_script, name='friend_script')
]
