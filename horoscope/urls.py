from django.urls import path

from . import views

app_name = 'horoscope'
urlpatterns = [
    path('', views.overview, name='index'),
    path('<int:sign_id>/', views.sign_overview, name='sign'),
    path('personal/', views.personal_sign, name='personal')
]
