from django.contrib import admin
from .models import Like, Comment, Share

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'video__title']
    readonly_fields = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'created_at', 'text_preview']
    list_filter = ['created_at']
    search_fields = ['user__username', 'video__title', 'text']
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'platform', 'created_at']
    list_filter = ['created_at', 'platform']
    search_fields = ['user__username', 'video__title', 'platform']
    readonly_fields = ['created_at']