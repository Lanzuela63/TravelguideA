# apps/dashboards/urls/admin_urls.py

from django.urls import path
from apps.dashboards.views.admin_views import admin_dashboard

app_name = "admin_dash"

urlpatterns = [
    path('', admin_dashboard, name="dashboard"),
]
