from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('video_analysis.urls')),  # Route root URL to myapp's URL configuration
]
