from django.shortcuts import render, get_object_or_404
from rest_framework import generics
import csv
from django.conf import settings
from apps.tourism.models import (
    TouristSpot, Category, Location, Review, Gallery, OperatingHour, ReportedSpot, TourismReportedSpotAlbay
)
from apps.tourism.serializers import (
    TouristSpotSerializer, CategorySerializer, LocationSerializer,
    ReviewSerializer, GallerySerializer, OperatingHourSerializer,
    TouristSpotDetailSerializer
)
from apps.tourism.filters import TouristSpotFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

# ============================================================
#                DRF GENERIC API VIEWS
# ============================================================

class TouristSpotListCreateView(generics.ListCreateAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer
    filterset_class = TouristSpotFilter


class TouristSpotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer


class TouristSpotFullDetailView(generics.RetrieveAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotDetailSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class GalleryListCreateView(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class GalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class OperatingHourListCreateView(generics.ListCreateAPIView):
    queryset = OperatingHour.objects.all()
    serializer_class = OperatingHourSerializer


class OperatingHourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OperatingHour.objects.all()
    serializer_class = OperatingHourSerializer


# ============================================================
#                FUNCTION-BASED PAGE VIEWS
# ============================================================

def public_home(request):
    featured_spots = TouristSpot.objects.filter(is_featured=True)
    return render(request, 'home/index.html', {
        'featured_spots': featured_spots
    })


def tourist_dashboard(request):
    spots = TouristSpot.objects.all()
    return render(request, 'dashboards/tourist_dashboard.html', {'spots': spots})


def explore_spots(request):
    search_query = request.GET.get('search', '')
    if search_query:
        spots = (TouristSpot.objects.filter(name__icontains=search_query) |
                 TouristSpot.objects.filter(location__name__icontains=search_query))
    else:
        spots = TouristSpot.objects.all()
    return render(request, 'tourism/explore_spots.html', {'spots': spots})


def spot_detail_view(request, pk):
    spot = get_object_or_404(TouristSpot, pk=pk)
    return render(request, 'tourism/spot_detail.html', {'spot': spot})


def saved_spots(request):
    return render(request, 'tourism/saved_spots.html', {})


def review_spots(request):
    return render(request, 'tourism/review_spots.html', {})


def reported_spots(request):
    query = request.GET.get('query', '')
    spots = TouristSpot.objects.filter(is_active=True)
    if query:
        spots = (spots.filter(name__icontains=query) |
                 spots.filter(description__icontains=query) |
                 spots.filter(category__name__icontains=query) |
                 spots.filter(location__name__icontains=query) |
                 spots.filter(location__region__icontains=query) |
                 spots.filter(location__province__icontains=query))
    categories = Category.objects.values_list('name', flat=True).distinct()
    return render(request, 'tourism/reported_spots_albay.html', {
        'spots': spots.distinct(),
        'query': query,
        'categories': categories,
    })


# ============================================================
#         REPORTED SPOTS BY PROVINCE (with CSV images)
# ============================================================

def _load_image_map():
    """Utility: Load spot ID -> image path mapping from CSV."""
    image_map = {}
    csv_path = settings.BASE_DIR / 'static' / 'tourism_reported_spots_albay.csv'

    def clean_image_path(raw):
        if not raw:
            return None
        fixed = raw.replace("\\", "/")
        marker = "shared/static/images/"
        idx = fixed.find(marker)
        if idx >= 0:
            fixed = fixed[idx + len(marker):]
        return f"images/{fixed.lstrip('/')}"

    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                img_path = clean_image_path(row.get('image'))
                try:
                    image_map[int(row['id'])] = img_path
                except (KeyError, ValueError):
                    continue
    except FileNotFoundError:
        pass

    return image_map

def reported_spots_albay_map(request, spot_id):
    # List of known Albay spot IDs you want to support
    albay_spot_ids = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12# <-- Replace with your known Albay spot IDs
    ]

    # Try to get the requested spot
    spot = TouristSpot.objects.filter(pk=spot_id, is_active=True).first()
    if not spot or spot.location.province.strip().lower() != "albay":
        from django.http import HttpResponse
        return HttpResponse(f"Spot ID {spot_id} not found or not in Albay.", status=404)

    # Hard-code the "more spots" as the rest of the list (excluding the requested one)
    more_spots = TouristSpot.objects.filter(
        pk__in=[sid for sid in albay_spot_ids if sid != spot_id],
        is_active=True
    )

    image_map = _load_image_map()
    spot_image = image_map.get(spot.id) or spot.image

    spot_data = {
        "name": spot.name,
        "description": spot.description,
        "image": spot_image,
        "category": spot.category.name if hasattr(spot.category, "name") else spot.category_id,
        "location": spot.location.name if hasattr(spot.location, "name") else "",
        "rating": getattr(spot, "rating", None),
        "embed_link": getattr(spot, "embed_link", None) or getattr(spot, "map_embed", None),
        "map_url": getattr(spot, "map_embed", None),
        "address": getattr(spot, "address", ""),
        "website": getattr(spot, "website", None),
    }

    return render(request, "tourism/reported_spots_albay_map.html", {
        "spot": spot_data,
        "more_spots": more_spots,
    })

# ============================================================
#   REPORTED SPOTS CAROUSEL + DETAIL (Albay, Camsur, Sorsogon)
# ============================================================

def reported_spots_albay_carousel(request):
    # Filter by province='Albay' and active spots
    albay_spots = TouristSpot.objects.filter(
        Q(is_active=True),
        location__province__iexact="Albay"
    )

    # Load external image map (your existing helper)
    image_map = _load_image_map()
    for spot in albay_spots:
        if image_map.get(spot.id):
            spot.image = image_map.get(spot.id)

    return render(request, "tourism/reported_spots_albay_carousel.html", {
        "spots": albay_spots,
    })


def reported_spots_albay_detail(request, pk: int):
    # Debugging logic to help diagnose 404 errors
    spots = TouristSpot.objects.select_related("location", "category").filter(pk=pk)
    if not spots.exists():
        from django.http import HttpResponse
        return HttpResponse(f"No spot with pk={pk} found.", status=404)
    spot = spots.first()
    province_clean = spot.location.province.strip().lower() if spot.location and spot.location.province else ""
    if not spot.is_active:
        from django.http import HttpResponse
        return HttpResponse(
            f"Spot found but not active: pk={pk}, is_active={spot.is_active}, province={spot.location.province!r}",
            status=404
        )
    if province_clean != "albay":
        from django.http import HttpResponse
        return HttpResponse(
            f"Spot found but province mismatch: pk={pk}, is_active={spot.is_active}, province={spot.location.province!r}",
            status=404
        )

    image_map = _load_image_map()
    spot_image = image_map.get(spot.id) or spot.image

    spot_data = {
        "name": spot.name,
        "description": spot.description,
        "image": spot_image,
        "category": spot.category.name if hasattr(spot.category, "name") else spot.category_id,
        "location": spot.location.name if hasattr(spot.location, "name") else "",
        "rating": getattr(spot, "rating", None),
        "map_url": getattr(spot, "map_embed", None),
        "address": getattr(spot, "address", ""),
        "website": getattr(spot, "website", None),
    }

    more_spots = (
        TouristSpot.objects
        .filter(location__province__iexact="Albay", is_active=True)
        .exclude(pk=pk)
        .order_by("name")[:8]
    )
    return render(request, "tourism/reported_spots_albay_map.html", {
        "spot": spot_data,
        "more_spots": more_spots,
    })


def reported_spots_camsur(request):
    query = request.GET.get('query', '')
    spots = TouristSpot.objects.filter(is_active=True)
    if query:
        spots = (spots.filter(name__icontains=query) |
                 spots.filter(description__icontains=query) |
                 spots.filter(category__name__icontains=query) |
                 spots.filter(location__name__icontains=query) |
                 spots.filter(location__region__icontains=query) |
                 spots.filter(location__province__iexact='Camarines Sur'))
    categories = Category.objects.values_list('name', flat=True).distinct()
    camsur_spots = TouristSpot.objects.filter(location__province__iexact='Camarines Sur', is_active=True)
    image_map = _load_image_map()
    for s in spots: s.image = image_map.get(s.id)
    for s in camsur_spots: s.image = image_map.get(s.id)
    return render(request, 'tourism/reported_spots_camsur.html', {
        'spots': spots.distinct(),
        'query': query,
        'categories': categories,
        'camsur_spots': camsur_spots,
    })


def reported_spots_sorsogon(request):
    query = request.GET.get('query', '')
    spots = TouristSpot.objects.filter(is_active=True)
    if query:
        spots = (spots.filter(name__icontains=query) |
                 spots.filter(description__icontains=query) |
                 spots.filter(category__name__icontains=query) |
                 spots.filter(location__name__icontains=query) |
                 spots.filter(location__region__icontains=query) |
                 spots.filter(location__province__iexact='Sorsogon'))
    categories = Category.objects.values_list('name', flat=True).distinct()
    sorsogon_spots = TouristSpot.objects.filter(location__province__iexact='Sorsogon', is_active=True)
    image_map = _load_image_map()
    for s in spots: s.image = image_map.get(s.id)
    for s in sorsogon_spots: s.image = image_map.get(s.id)
    return render(request, 'tourism/reported_spots_sorsogon.html', {
        'spots': spots.distinct(),
        'query': query,
        'categories': categories,
        'sorsogon_spots': sorsogon_spots,
    })


def reported_spots_albay(request):
    query = request.GET.get('query', '')
    spots = TouristSpot.objects.filter(is_active=True)
    if query:
        spots = (spots.filter(name__icontains=query) |
                 spots.filter(description__icontains=query) |
                 spots.filter(category__name__icontains=query) |
                 spots.filter(location__name__icontains=query) |
                 spots.filter(location__region__icontains=query) |
                 spots.filter(location__province__iexact='Albay'))
    categories = Category.objects.values_list('name', flat=True).distinct()
    albay_spots = TouristSpot.objects.filter(location__province__iexact='Albay', is_active=True)
    image_map = _load_image_map()
    for s in spots: s.image = image_map.get(s.id)
    for s in albay_spots: s.image = image_map.get(s.id)
    return render(request, 'tourism/reported_spots_albay.html', {
        'spots': spots.distinct(),
        'query': query,
        'categories': categories,
        'albay_spots': albay_spots,
    })


# ============================================================
#              TOURIST SPOT LIST/DETAIL (general)
# ============================================================

def tourist_spot_list(request):
    spots = TouristSpot.objects.all()
    return render(request, "tourism/tourist_spot_list.html", {"spots": spots})


def tourist_spot_detail(request, pk):
    spot = get_object_or_404(TouristSpot, pk=pk)
    return render(request, "tourism/tourist_spot_detail.html", {"spot": spot})


# ============================================================
#              REPORTED SPOTS (LEGACY LIST)
# ============================================================

def reported_spots_albay_list(request):
    spots = ReportedSpot.objects.filter(province__iexact="Albay")
    return render(request, "tourism/reported_spots_albay_list.html", {"spots": spots})