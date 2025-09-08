import os
import csv
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from django.conf import settings
from django.http import JsonResponse, Http404
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
    categories = Category.objects.all().order_by("id")
    return render(request, 'tourism/reported_spots_albay.html', {
        'spots': spots.distinct(),
        'query': query,
        'categories': categories,
    })


# ============================================================
#         REPORTED SPOTS BY PROVINCE (with CSV images)
# ============================================================

def _load_image_map():
    image_map = {}
    csv_path = os.path.join(settings.BASE_DIR, "shared", "static", "tourism_touristspot.csv")

    def clean_image_path(raw):
        if not raw:
            return None
        fixed = raw.replace("\\", "/")
        marker = "shared/static/images/"
        idx = fixed.find(marker)
        if idx >= 0:
            fixed = fixed[idx + len(marker):]
        # ✅ Prevent double "images/" prefix
        if fixed.startswith("images/"):
            return fixed
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


def load_csv_dict(file_path, key_field):
    """Helper to load a csv into a dict by key_field."""
    result = {}
    try:
        with open(file_path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                result[row[key_field]] = row
    except Exception:
        pass
    return result

def build_spot(row, province, locations=None, categories=None):
    # Build a spot dict, resolving location/category if possible.
    location = locations.get(row.get("location_id")) if locations else {}
    category = categories.get(row.get("category_id")) if categories else {}

    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "description": row.get("description"),
        "image": row.get("image"),
        "rating": row.get("rating"),
        "address": row.get("address"),
        "map_embed": row.get("map_embed"),
        "category": category.get("name") if category else "",
        "category_id": row.get("category_id"),
        "location": location.get("name") if location else "",
        "province": location.get("province") if location else province,
        "region": location.get("region") if location else "",
        "location_id": row.get("location_id"),
        # You can add more fields if needed
    }

def reported_spots_albay_map(request, name_url=None):
    base = os.path.join(settings.BASE_DIR, "shared", "static")
    spot_csv = os.path.join(base, "tourism_touristspot.csv")
    cat_csv = os.path.join(base, "tourism_touristspot_category.csv")
    loc_csv = os.path.join(base, "tourism_location.csv")

    # Load categories
    categories = {}
    with open(cat_csv, newline='', encoding='utf-8') as cat_file:
        for row in csv.DictReader(cat_file):
            categories[row['id']] = row['name']

    # Load locations
    locations = {}
    with open(loc_csv, newline='', encoding='utf-8') as loc_file:
        for row in csv.DictReader(loc_file):
            locations[row['id']] = row

    selected_spot = None
    with open(spot_csv, newline='', encoding='utf-8') as spot_file:
        for row in csv.DictReader(spot_file):
            loc = locations.get(row['location_id'])
            if not loc or loc['province'].strip().lower() != 'albay':
                continue
            if name_url and row.get('name_url') != name_url:
                continue
            # Found our spot or just the first one if no name_url
            selected_spot = {
                "name": row["name"],
                "description": row["description"],
                "image": row["image"],
                "rating": row["rating"],
                "category": categories.get(row["category_id"], ""),
                "address": row.get("address") or f"{loc.get('name', '')}, {loc.get('province', '')}, {loc.get('region', '')}",
                "website": row.get("website", ""),
                "map_embed": clean_map_src(row.get("map_embed", "")),
            }
            break

    return render(request, "tourism/reported_spots_albay_map.html", {
        "spot": selected_spot
    })

# ============================================================
#   REPORTED SPOTS CAROUSEL + DETAIL (Albay, Camsur, Sorsogon)
# ============================================================

def reported_spots_albay_carousel(request):
    spots = []
    base = os.path.join(settings.BASE_DIR, "shared", "static")
    spot_csv = os.path.join(base, "tourism_touristspot.csv")
    loc_csv = os.path.join(base, "tourism_location.csv")
    cat_csv = os.path.join(base, "tourism_touristspot_category.csv")

    # Load relational data
    locations = load_csv_dict(loc_csv, "id")
    categories = load_csv_dict(cat_csv, "id")

    with open(spot_csv, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Find province via location
            loc = locations.get(row.get("location_id"))
            province = loc.get("province", "").strip().lower() if loc else row.get("province", "").strip().lower()
            if province != "albay":
                continue
            if not row.get("id", "").strip() or not row.get("name", "").strip():
                continue
            spots.append(build_spot(row, "albay", locations, categories))

    return render(request, "tourism/reported_spots_albay_carousel.html", {"spots": spots})

def reported_spots_albay_detail(request, name_url):
    spot_data = None
    more_spots = []
    try:
        # Try database
        spot = TouristSpot.objects.select_related("category", "location").get(
            is_active=True,
            location__province__iexact="Albay",
            name_url=name_url
        )
        image_map = _load_image_map()
        spot.image = image_map.get(spot.id) or spot.image

        spot_data = {
            "name": spot.name,
            "description": spot.description,
            "image": spot.image,
            "name_url": spot.name_url,
            "category": spot.category.name if hasattr(spot.category, "name") else spot.category_id,
            "rating": getattr(spot, "rating", None),
            "map_embed": getattr(spot, "map_embed", None),
            "address": f"{spot.location.name}, {spot.location.province}, {spot.location.region}",
            "social_media_link": spot.website,
        }

        more_spots = TouristSpot.objects.filter(
            is_active=True,
            location__province__iexact="Albay"
        ).exclude(id=spot.id)
    except Exception:
        # Fallback: search CSV
        base = os.path.join(settings.BASE_DIR, "shared", "static")
        spot_csv = os.path.join(base, "tourism_touristspot.csv")
        loc_csv = os.path.join(base, "tourism_location.csv")
        cat_csv = os.path.join(base, "tourism_touristspot_category.csv")

        locations = load_csv_dict(loc_csv, "id")
        categories = load_csv_dict(cat_csv, "id")
        spot_data = None

        try:
            with open(spot_csv, encoding="utf-8") as spotfile:
                for row in csv.DictReader(spotfile):
                    if row.get("name_url") == name_url:
                        loc = locations.get(row.get("location_id"))
                        province = loc.get("province", "").strip().lower() if loc else row.get("province", "").strip().lower()
                        if province != "albay":
                            continue
                        cat_name = categories.get(row.get("category_id"), {}).get("name", "")
                        spot_data = build_spot(row, "albay", locations, categories)
                        break
        except Exception:
            spot_data = None

        # Get more spots for sidebar/carousel (from CSV)
        more_spots = []
        if spot_data:
            try:
                with open(spot_csv, encoding="utf-8") as spotfile:
                    for row in csv.DictReader(spotfile):
                        loc = locations.get(row.get("location_id"))
                        province = loc.get("province", "").strip().lower() if loc else row.get("province", "").strip().lower()
                        if province != "albay":
                            continue
                        if row.get("name_url") != name_url:
                            more_spots.append(build_spot(row, "albay", locations, categories))
            except Exception:
                more_spots = []

        if not spot_data:
            raise Http404("No TouristSpot matches the given query.")

    # Render or return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(spot_data)
    else:
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
    spots = TouristSpot.objects.filter(is_active=True, location__province__iexact='Albay')

    if query and query.lower() != "all":
        spots = spots.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__name__icontains=query) |
            Q(category__name__icontains=query)  # ✅ category join
        )

    categories = Category.objects.all().order_by("id")

    image_map = _load_image_map()
    for s in spots:
        s.image = image_map.get(s.id) or s.image

    return render(request, 'tourism/reported_spots_albay.html', {
        'spots': spots.distinct(),
        'query': query,
        'categories': categories,
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