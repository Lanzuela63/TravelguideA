from django.urls import include, path

urlpatterns = [
    path('admin/', include('apps.dashboards.urls.admin_urls')),
    path('tourist/', include('apps.dashboards.urls.tourist_urls')),
    path('business/', include('apps.dashboards.urls.business_urls')),
    path('event/', include('apps.dashboards.urls.event_urls')),
    path('tourism/', include('apps.dashboards.urls.tourism_urls')),
]