# apps/dashboards/views/business_views.py

from django.shortcuts import render
from apps.business.models import Business
from apps.dashboards.views.cards_utils import get_dashboard_cards

def business_dashboard(request):
    pending_businesses = Business.objects.filter(owner=request.user, is_approved=False)[:10]
    dashboard_cards = get_dashboard_cards("Business Owner")
    return render(request, "dashboards/business_dashboard.html", {
        "dashboard_cards": dashboard_cards,
        "pending_businesses": pending_businesses,

    })

