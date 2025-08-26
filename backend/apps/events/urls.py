#apps/events/urls.py

from django.urls import path
from apps.events.views.main_views import manage_events, create_event

app_name = "events"
urlpatterns = [
    path('manage/', manage_events, name='manage_events'),
    path('create/', create_event, name='create_event'),
]
