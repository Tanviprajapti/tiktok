from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, CreatorRegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    
    context = {
        'u_form': u_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def become_creator(request):
    if request.user.is_creator:
        messages.warning(request, 'You are already a creator!')
        return redirect('profile')
    
    if request.method == 'POST':
        form = CreatorRegistrationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_creator = True
            user.save()
            messages.success(request, 'You are now a creator! You can upload videos.')
            return redirect('videos:video_upload')
    else:
        form = CreatorRegistrationForm(instance=request.user)
    
    return render(request, 'users/become_creator.html', {'form': form})
from django.contrib.auth import logout
def custom_logout(request):
    logout(request)  # Ends the user session
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  