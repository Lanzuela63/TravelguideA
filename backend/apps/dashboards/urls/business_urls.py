# apps/dashboards/urls/business_urls.py

from django.urls import path
from apps.dashboards.views.business_views import business_dashboard

app_name = "business_dash"

urlpatterns = [
    path('', business_dashboard, name="dashboard"),
]
