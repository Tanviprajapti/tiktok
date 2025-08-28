from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core.videos import views as video_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', video_views.home, name='home'),
    path('videos/', include('core.videos.urls')),
    path('interactions/', include('core.interactions.urls')),
    path('users/', include('core.users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)