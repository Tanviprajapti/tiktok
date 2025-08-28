from django.urls import path
from . import views

urlpatterns = [
    path('like/<uuid:video_id>/', views.like_video, name='like_video'),
    path('comment/<uuid:video_id>/', views.add_comment, name='add_comment'),
    path('share/<uuid:video_id>/', views.share_video, name='share_video'),
]