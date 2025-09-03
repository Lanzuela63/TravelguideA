from django.shortcuts import render, get_object_or_404
from rest_framework import generics
import csv
import os
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

def reported_spots_albay_map(request):
    # --- Search/filter functionality ---
    query = request.GET.get('query', '').strip().lower()
    static_folder = os.path.join(settings.BASE_DIR, "shared", "static")
    spot_csv = os.path.join(static_folder, "tourism_touristspot.csv")
    loc_csv = os.path.join(static_folder, "tourism_location.csv")
    cat_csv = os.path.join(static_folder, "tourism_touristspot_category.csv")

    # --- Load locations ---
    locations = {}
    with open(loc_csv, encoding="utf-8") as locfile:
        for row in csv.DictReader(locfile):
            locations[row["id"]] = row

    # --- Load categories ---
    categories = {}
    with open(cat_csv, encoding="utf-8") as catfile:
        for row in csv.DictReader(catfile):
            categories[row["id"]] = row["name"]

    # --- Load all spots ---
    albay_spots = []
    all_categories = set()
    with open(spot_csv, encoding="utf-8") as spotfile:
        for row in csv.DictReader(spotfile):
            loc = locations.get(row["location_id"])
            if not loc or loc["province"].lower() != "albay":
                continue
            cat_name = categories.get(row["category_id"], "")
            all_categories.add(cat_name)

            # --- Search filter logic (matches name, desc, category, location) ---
            if query:
                match = (
                    query in row["name"].lower() or
                    query in row["description"].lower() or
                    query in cat_name.lower() or
                    query in loc["name"].lower() or
                    query in loc["region"].lower() or
                    query in loc["province"].lower()
                )
                if not match:
                    continue

            albay_spots.append({
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "image": row["image"],  # Use for header image
                "rating": row["rating"],
                "address": row["address"],
                "map_embed": row["map_embed"],  # Use for embedded map (iframe HTML)
                "category": cat_name,
                "location": loc["name"],
                "province": loc["province"],
                "region": loc["region"],
            })

    # --- Pass categories and spots to template for display ---
    return render(request, "tourism/reported_spots_albay_map.html", {
        "albay_spots": albay_spots,
        "query": request.GET.get('query', ''),
        "categories": sorted(all_categories),
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
            "map_url": getattr(spot, "map_embed", None),
            "address": f"{spot.location.name}, {spot.location.province}, {spot.location.region}",
            "social_media_link": spot.website,
        }

        more_spots = TouristSpot.objects.filter(
            is_active=True,
            location__province__iexact="Albay"
        ).exclude(id=spot.id)
    except Exception:
        # Fallback: search CSV
        static_folder = os.path.join(settings.BASE_DIR, "shared", "static")
        spot_csv = os.path.join(static_folder, "tourism_touristspot.csv")
        loc_csv = os.path.join(static_folder, "tourism_location.csv")
        cat_csv = os.path.join(static_folder, "tourism_touristspot_category.csv")

        locations = {}
        try:
            with open(loc_csv, encoding="utf-8") as locfile:
                for row in csv.DictReader(locfile):
                    locations[row["id"]] = row
        except Exception as e:
            locations = {}

        categories = {}
        try:
            with open(cat_csv, encoding="utf-8") as catfile:
                for row in csv.DictReader(catfile):
                    categories[row["id"]] = row["name"]
        except Exception as e:
            categories = {}

        spot_data = None
        try:
            with open(spot_csv, encoding="utf-8") as spotfile:
                for row in csv.DictReader(spotfile):
                    if row["name_url"] == name_url:
                        loc = locations.get(row["location_id"])
                        if not loc or loc["province"].lower() != "albay":
                            continue
                        cat_name = categories.get(row["category_id"], "")
                        spot_data = {
                            "name": row["name"],
                            "description": row["description"],
                            "image": row["image"],
                            "name_url": row["name_url"],
                            "category": cat_name,
                            "rating": row["rating"],
                            "map_url": row["map_embed"],
                            "address": row["address"],
                            "social_media_link": row["website"],
                        }
                        break
        except Exception as e:
            spot_data = None

        # Get more spots for sidebar/carousel (from CSV)
        more_spots = []
        if spot_data:
            try:
                with open(spot_csv, encoding="utf-8") as spotfile:
                    for row in csv.DictReader(spotfile):
                        loc = locations.get(row["location_id"])
                        if not loc or loc["province"].lower() != "albay":
                            continue
                        if row["name_url"] != name_url:
                            cat_name = categories.get(row["category_id"], "")
                            more_spots.append({
                                "name": row["name"],
                                "description": row["description"],
                                "image": row["image"],
                                "name_url": row["name_url"],
                                "category": cat_name,
                                "rating": row["rating"],
                                "map_url": row["map_embed"],
                                "address": row["address"],
                                "social_media_link": row["website"],
                            })
            except Exception as e:
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