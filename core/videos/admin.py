from django.contrib import admin
from .models import Video, VideoView

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'view_count', 'like_count', 'comment_count']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'like_count', 'comment_count']
    fieldsets = [
        ('Basic Information', {
            'fields': ['user', 'title', 'description']
        }),
        ('Media', {
            'fields': ['video_file', 'youtube_url', 'thumbnail']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
        ('Statistics', {
            'fields': ['view_count', 'like_count', 'comment_count'],
            'classes': ['collapse']
        })
    ]

@admin.register(VideoView)
class VideoViewAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['video__title', 'user__username']
    readonly_fields = ['created_at']