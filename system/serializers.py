from django.urls import path, include
from system.models import Score
from rest_framework import routers, serializers, viewsets

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('user', 'score', 'lesson_name', 'time','summary')