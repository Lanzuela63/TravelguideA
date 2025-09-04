import csv
import os
import re
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def clean_map_src(raw_value):
    """
    Cleans up the map_src/embed_link value from CSV.
    - If it's a full <iframe ...>, extract only the src URL.
    - Otherwise, return it as-is (already a URL).
    """
    if not raw_value:
        return ""
    match = re.search(r'src="([^"]+)"', raw_value)
    if match:
        return match.group(1)
    return raw_value.strip()


def build_spot(row, province, locations=None, categories=None):
    """Build a spot dict, resolving location/category if possible."""
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


@login_required
def explore_spots(request):
    return render(request, 'tourism/explore_spots.html')


@login_required
def saved_spots(request):
    return render(request, 'tourism/saved_spots.html')


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


def reported_spots_camsur_carousel(request):
    spots = []
    csv_path = os.path.join(settings.BASE_DIR, "shared", "static", "tourism_reported_spots_camsur.csv")

    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("province", "").strip().lower() not in ["camarines sur", "camsur"]:
                continue
            if not row.get("id", "").strip() or not row.get("name", "").strip():
                continue
            spots.append(build_spot(row, "camsur"))

    return render(request, "tourism/reported_spots_camsur_carousel.html", {"spots": spots})


def reported_spots_sorsogon_carousel(request):
    spots = []
    csv_path = os.path.join(settings.BASE_DIR, "shared", "static", "tourism_reported_spots_sorsogon.csv")

    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("province", "").strip().lower() != "sorsogon":
                continue
            if not row.get("id", "").strip() or not row.get("name", "").strip():
                continue
            spots.append(build_spot(row, "sorsogon"))

    return render(request, "tourism/reported_spots_sorsogon_carousel.html", {"spots": spots})

def reported_spots_albay_map(request, spot_id):
    """
    Expanded view for a single Albay tourist spot with map included.
    """
    base = os.path.join(settings.BASE_DIR, "shared", "static")
    spot_csv = os.path.join(base, "tourism_touristspot.csv")
    loc_csv = os.path.join(base, "tourism_location.csv")
    cat_csv = os.path.join(base, "tourism_touristspot_category.csv")

    locations = load_csv_dict(loc_csv, "id")
    categories = load_csv_dict(cat_csv, "id")
    spot = None

    with open(spot_csv, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            loc = locations.get(row.get("location_id"))
            province = loc.get("province", "").strip().lower() if loc else row.get("province", "").strip().lower()
            if province != "albay":
                continue

            if row.get("id", "").strip() == str(spot_id):
                spot = build_spot(row, "albay", locations, categories)
                break

    if not spot:
        return render(request, "404.html", status=404)

    return render(request, "tourism/reported_spots_albay_map.html", {"spot": spot})

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