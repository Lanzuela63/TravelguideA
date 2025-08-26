# apps/dashboards/views/event_views.py

from django.shortcuts import render
from django.utils.timezone import now
from apps.events.models import Event
from apps.dashboards.views.cards_utils import get_dashboard_cards

def event_dashboard(request):
    upcoming_events = Event.objects.filter(organizer=request.user, date__gte=now()).order_by("date")[:10]
    dashboard_cards = get_dashboard_cards("Event Organizer")
    return render(request, "dashboards/event_dashboard.html", {
        "dashboard_cards": dashboard_cards,
        "upcoming_events": upcoming_events,
    })

