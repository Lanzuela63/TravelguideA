from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.tourism.views import main_views, tourist_views

app_name = "tourism"

from apps.tourism.views.main_views import (
    TouristSpotListCreateView, TouristSpotDetailView,
    CategoryListCreateView, CategoryDetailView,
    LocationListCreateView, LocationDetailView,
    ReviewListCreateView, ReviewDetailView,
    GalleryListCreateView, GalleryDetailView,
    OperatingHourListCreateView, OperatingHourDetailView,
    TouristSpotFullDetailView, public_home,
    spot_detail_view, explore_spots, saved_spots, review_spots,
    reported_spots,
    reported_spots_albay,      # Combined Albay view (search+carousel)
    reported_spots_camsur,     # Combined CamSur view
    reported_spots_sorsogon,   # Combined Sorsogon view
)

from apps.tourism.views.api_views import TouristSpotListAPIView, list_tourist_spots

app_name = "tourism"

urlpatterns = [
    path('tourist-spots/', TouristSpotListAPIView.as_view()),
    path('spots/', TouristSpotListCreateView.as_view(), name='spot-list-create'),
    path('spots/<int:pk>/', TouristSpotDetailView.as_view(), name='spot-detail'),
    path('spots/<int:pk>/full/', TouristSpotFullDetailView.as_view(), name='spot-full-detail'),
    path("spots/", main_views.tourist_spot_list, name="tourist_spot_list"),
    path("spots/<int:pk>/", main_views.tourist_spot_detail, name="tourist_spot_detail"),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    path('galleries/', GalleryListCreateView.as_view(), name='gallery-list-create'),
    path('galleries/<int:pk>/', GalleryDetailView.as_view(), name='gallery-detail'),

    path('hours/', OperatingHourListCreateView.as_view(), name='operatinghour-list-create'),
    path('hours/<int:pk>/', OperatingHourDetailView.as_view(), name='operatinghour-detail'),
    path('', public_home, name='public-home'),

    path('spots/<int:pk>/view/', spot_detail_view, name='spot-detail-view'),

    path('explore/', explore_spots, name='explore_spots'),
    path('saved/', saved_spots, name='saved_spots'),
    path('review/', review_spots, name='review_spots'),

    # Search/filter page for reported spots (province-agnostic)
    path('reports/', reported_spots, name='reported_spots'),

    # Combined province views (search/filter + carousel)
    path('reports/albay/', reported_spots_albay, name='reported_spots_albay'),
    path('reports/camsur/', reported_spots_camsur, name='reported_spots_camsur'),
    path('reports/sorsogon/', reported_spots_sorsogon, name='reported_spots_sorsogon'),
    path("explore/", tourist_views.explore_spots, name="explore_spots"),
    path("saved/", tourist_views.saved_spots, name="saved_spots"),
    path("reported-spots/albay/", main_views.reported_spots_albay_carousel, name="reported_spots_albay_carousel"),
    path("reports/albay/<int:pk>/", main_views.reported_spots_albay_detail, name="reported_spot_albay_detail"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
