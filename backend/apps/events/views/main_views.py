from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def manage_events(request):
    return render(request, 'events/manage_events.html')

@login_required
def create_event(request):
    return render(request, "events/create_event.html")
