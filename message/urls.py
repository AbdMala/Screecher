from django.urls import path

from . import views

app_name = 'message'
urlpatterns = [
    path('inbox/', views.inbox, name='index'),
    path('outbox/', views.outbox, name='outbox'),
    path('store/', views.store_message, name='store'),
    path('delete/', views.delete_message, name='delete'),
    path('read/', views.mark_as_read, name='read'),
    path('ignore/', views.ignore_message, name='ignore')
]
