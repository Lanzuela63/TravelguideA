#apps/business/urls.py

from django.urls import path
from apps.business.views.main_views import business_listings, add_business

app_name = "business"

urlpatterns = [
    path('listings/', business_listings, name='business_listings'),
    path('add/', add_business, name='add_business'),
]
