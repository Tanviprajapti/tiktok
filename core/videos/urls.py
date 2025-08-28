from django.urls import path
from . import views
app_name = 'videos'
urlpatterns = [
    path('', views.home, name='home'),
    path('video/<uuid:video_id>/', views.video_detail, name='video_detail'),
    path('upload/', views.video_upload, name='video_upload'),
    path('video/<uuid:video_id>/like/', views.video_like, name='video_like'),
    path('video/<uuid:video_id>/comment/', views.video_comment, name='video_comment'),
]