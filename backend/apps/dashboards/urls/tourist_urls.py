# apps/dashboards/urls/tourist_urls.py

from django.urls import path
from apps.dashboards.views.tourist_views import tourist_dashboard

app_name = "tourist_dash"

urlpatterns = [
    path('', tourist_dashboard, name="dashboard"),
    #path('cards/', tourist_dashboard, name="cards"), # HTMX partial
]
