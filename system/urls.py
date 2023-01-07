from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

app_name = 'system'

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
]