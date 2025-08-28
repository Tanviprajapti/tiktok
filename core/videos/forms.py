from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'youtube_url', 'thumbnail']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }