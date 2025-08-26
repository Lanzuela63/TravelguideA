from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from apps.users.forms import CustomUserUpdateForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def view_profile(request):
    return render(request, 'users/view_profile.html', {'user': request.user})