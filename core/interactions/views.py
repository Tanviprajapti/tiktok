from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Like, Comment, Share
from core.videos.models import Video

@login_required
@require_POST
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    like, created = Like.objects.get_or_create(video=video, user=request.user)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({'liked': liked, 'like_count': video.like_count})

@login_required
@require_POST
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    text = request.POST.get('text', '').strip()
    
    if text:
        comment = Comment.objects.create(video=video, user=request.user, text=text)
        return JsonResponse({
            'success': True,
            'comment': {
                'text': comment.text,
                'user': comment.user.username,
                'avatar_url': comment.user.avatar.url if comment.user.avatar else '',
                'created_at': comment.created_at.strftime('%b %d, %Y')
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})

@login_required
def share_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    platform = request.GET.get('platform', 'copy_link')
    
    Share.objects.create(video=video, user=request.user, platform=platform)
    
    # Return appropriate response based on platform
    if platform == 'copy_link':
        return JsonResponse({'success': True, 'message': 'Link copied to clipboard'})
    else:
        # In a real implementation, you would redirect to the sharing platform
        return JsonResponse({'success': True, 'message': f'Shared on {platform}'})