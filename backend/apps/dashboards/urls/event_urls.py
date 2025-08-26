# apps/dashboards/urls/event_urls.py

from django.urls import path
from apps.dashboards.views.event_views import event_dashboard

app_name = "event_dash"

urlpatterns = [
    path('', event_dashboard, name="dashboard"),
]
