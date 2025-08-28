from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from core.videos.models import Video
import os

class Command(BaseCommand):
    help = 'Migrate media files to Azure Storage'
    
    def handle(self, *args, **options):
        if not hasattr(default_storage, 'azure_container'):
            self.stdout.write('Azure storage not configured. Skipping migration.')
            return
            
        videos = Video.objects.all()
        for video in videos:
            if video.video_file and video.video_file.name:
                try:
                    with open(video.video_file.path, 'rb') as f:
                        default_storage.save(video.video_file.name, f)
                    self.stdout.write(f'Migrated video: {video.video_file.name}')
                except FileNotFoundError:
                    self.stdout.write(f'Video file not found: {video.video_file.name}')
                except Exception as e:
                    self.stdout.write(f'Error migrating video {video.video_file.name}: {str(e)}')
            
            if video.thumbnail and video.thumbnail.name:
                try:
                    with open(video.thumbnail.path, 'rb') as f:
                        default_storage.save(video.thumbnail.name, f)
                    self.stdout.write(f'Migrated thumbnail: {video.thumbnail.name}')
                except FileNotFoundError:
                    self.stdout.write(f'Thumbnail file not found: {video.thumbnail.name}')
                except Exception as e:
                    self.stdout.write(f'Error migrating thumbnail {video.thumbnail.name}: {str(e)}')
        
        self.stdout.write('Media migration completed.')
