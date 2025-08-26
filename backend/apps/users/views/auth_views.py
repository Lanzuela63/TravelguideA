#apps/users/views/auth_views.py
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from apps.users.forms import CustomUserCreationForm
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers.auth_serializers import CustomTokenObtainPairSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    user = request.user
    role = user.groups.first().name if user.groups.exists() else "Unknown"
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role,
        }
    )

# Web Views – HTML Based
def login_view(request):  # This block in login_view() handles role-based redirecting:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")

            # If Valid credentials,  Role-based redirect
            groups = user.groups.values_list("name", flat=True)
            if "Admin" in groups:
                return redirect("admin_dash:dashboard")
            elif "Tourism Officer" in groups:
                return redirect("tourism_dash:dashboard")
            elif "Business Owner" in groups:
                return redirect("business_dash:dashboard")
            elif "Event Organizer" in groups:
                return redirect("event_dash:dashboard")
            elif "Tourist" in groups:
                return redirect("tourist_dash:dashboard")
            else:
                return redirect("public-home")  # fallback for ungrouped users
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})

# User Registration
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        role = request.POST.get("role")

        if form.is_valid():
            user = form.save()
            if role:
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("public-home")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            print(form.errors)  # Temporary debug: view terminal for details
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/register.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("public-home")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer