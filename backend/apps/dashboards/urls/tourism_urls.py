# apps/dashboards/urls/tourism_urls.py

from django.urls import path
from apps.dashboards.views.tourism_views import tourism_dashboard

app_name = "tourism_dash"

urlpatterns = [
    path('', tourism_dashboard, name="dashboard"),
]
