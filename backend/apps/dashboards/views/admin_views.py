# apps/dashboards/views/admin_views.py

from django.shortcuts import render
from apps.tourism.models import TouristSpot
from apps.dashboards.views.cards_utils import get_dashboard_cards

def admin_dashboard(request):
    approved_spots = TouristSpot.objects.filter(is_active=True).select_related("location")[:10]
    dashboard_cards = get_dashboard_cards("Admin")
    return render(request, "dashboards/admin_dashboard.html", {
        "dashboard_cards": dashboard_cards,
        "approved_spots": approved_spots,
    })
