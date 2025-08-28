from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_creator', 'date_joined', 'video_count']
    list_filter = ['is_creator', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'bio']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('is_creator', 'avatar', 'bio')
        }),
    )
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'