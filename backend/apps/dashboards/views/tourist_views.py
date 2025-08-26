# apps/dashboards/views/tourist_views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.tourism.models import TouristSpot
from apps.dashboards.views.cards_utils import get_dashboard_cards

from apps.tourism.models import SavedSpot, VisitedSpot

@login_required
def tourist_dashboard(request):
    user = request.user

    # Real-time stats
    approved_spots_count = TouristSpot.objects.filter(is_active=True).count()
    saved_spots_count = SavedSpot.objects.filter(user=user).count() # if hasattr(user, 'savedspot_set') else 0
    visited_spots_count = VisitedSpot.objects.filter(user=user).count() # if hasattr(user, 'visitedspot_set') else 0

    # Featured spots for display
    featured_spots = TouristSpot.objects.filter(is_active=True, is_featured=True).order_by("-created_at")[:10]

    # Dashboard cards (use card_utils logic)
    dashboard_cards = get_dashboard_cards("Tourist")

    return render(request, "dashboards/tourist_dashboard.html", {
        "dashboard_cards": dashboard_cards,
        "featured_spots": featured_spots,
        "approved_spots_count": approved_spots_count,
        "saved_spots_count": saved_spots_count,
        "visited_spots_count": visited_spots_count,
    })


