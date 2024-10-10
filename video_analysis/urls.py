from django.urls import path
from .views import video_upload

urlpatterns = [
    path('video-upload/', video_upload, name='video_upload'),
]