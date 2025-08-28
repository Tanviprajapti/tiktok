from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Video, VideoView
from .forms import VideoForm
from core.interactions.models import Like, Comment
from core.interactions.forms import CommentForm

def home(request):
    # Get search query
    search_query = request.GET.get('q', '')
    
    # Filter videos based on search query
    if search_query:
        videos = Video.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(user__username__icontains=search_query)
        ).order_by('-created_at')
    else:
        videos = Video.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(videos, 12)  # Show 12 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'videos/home.html', context)

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Track view
    if request.user.is_authenticated:
        VideoView.objects.get_or_create(video=video, user=request.user)
    else:
        # For anonymous users, we could track by session
        VideoView.objects.get_or_create(video=video, user=None)
    
    # Comment form
    comment_form = CommentForm()
    comments = video.comments.all().order_by('-created_at')
    
    # Check if user liked the video
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(video=video, user=request.user).exists()
    
    # Get related videos (videos from the same user)
    related_videos = Video.objects.filter(user=video.user).exclude(id=video.id).order_by('-created_at')[:6]
    
    return render(request, 'videos/video_detail.html', {
        'video': video,
        'comment_form': comment_form,
        'comments': comments,
        'user_liked': user_liked,
        'related_videos': related_videos,
    })

@login_required
def video_upload(request):
    if not request.user.is_creator:
        messages.warning(request, 'You need to be a creator to upload videos.')
        return redirect('users:become_creator')
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, 'Your video has been uploaded!')
            return redirect('videos:video_detail', video_id=video.id)
    else:
        form = VideoForm()
    
    return render(request, 'videos/video_upload.html', {'form': form})

@login_required
@require_POST
def video_like(request, video_id):
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
def video_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.video = video
        comment.save()
        
        return JsonResponse({
            'success': True,
            'comment': {
                'text': comment.text,
                'user': comment.user.username,
                'created_at': comment.created_at.strftime('%b %d, %Y')
            }
        })
    
    return JsonResponse({'success': False, 'errors': form.errors})