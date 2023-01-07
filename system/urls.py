from django.urls import path

from system.filters import ScoreFilter
from . import views

app_name = 'system'

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('progress/', views.ScoreListView.as_view(filterset_class=ScoreFilter), name='progress'),
]