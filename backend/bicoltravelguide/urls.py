# bicoltravelguide/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.tourism.views.api_views import TouristSpotListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public and auth routes
    path('', include('apps.users.urls')),

    # Tourism app routes with namespace
    path("tourism/", include(("apps.tourism.urls", "tourism"), namespace="tourism")),

    # API routes
    path('api/tourism-spots/', TouristSpotListAPIView.as_view(), name='tourism-spot-list'),

    # Business app routes with namespace
    path("business/", include(("apps.business.urls", "businesses"), namespace="businesses")),

    # Events app routes with namespace
    path("events/", include(("apps.events.urls", "events"), namespace="events")),

    # AR app routes with namespace
    path("ar/", include("apps.ar.urls", namespace="ar")),

    # Modular dashboards with unique namespaces
    path('dashboard/admin/', include(('apps.dashboards.urls.admin_urls', 'admin_dash'), namespace='admin_dash')),
    path('dashboard/tourism/',
         include(('apps.dashboards.urls.tourism_urls', 'tourism_dash'), namespace='tourism_dash')),
    path('dashboard/business/',
         include(('apps.dashboards.urls.business_urls', 'business_dash'), namespace='business_dash')),
    path('dashboard/event/', include(('apps.dashboards.urls.event_urls', 'event_dash'), namespace='event_dash')),
    path('dashboard/tourist/',
         include(('apps.dashboards.urls.tourist_urls', 'tourist_dash'), namespace='tourist_dash')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)