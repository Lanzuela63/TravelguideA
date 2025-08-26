# apps/dashboards/views/tourism_views.py

from django.shortcuts import render
from apps.tourism.models import TouristSpot
from apps.dashboards.views.cards_utils import get_dashboard_cards

def tourism_dashboard(request):
    pending_spots = TouristSpot.objects.filter(is_active=False).select_related("location")[:10]
    dashboard_cards = get_dashboard_cards("Tourism Officer")
    return render(request, "dashboards/tourism_dashboard.html", {
        "dashboard_cards": dashboard_cards,
        "pending_spots": pending_spots,
    })


