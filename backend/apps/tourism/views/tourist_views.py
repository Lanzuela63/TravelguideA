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


def build_spot(row, province_folder):
    """Builds a dictionary for a tourist spot from CSV row."""
    name = row.get("name", "").strip()

    # Try map_src first, then embed_link
    raw_map = row.get("map_src", "").strip() or row.get("map_url", "").strip()

    return {
        "id": row.get("id", "").strip(),
        "image": f"images/reported_spots/{province_folder}/{name}.jpg",
        "name": name,
        "description": row.get("description", "").strip(),
        "category": row.get("category_name", "").strip(),
        "location": row.get("location_name", "").strip(),
        "rating": row.get("rating", "").strip() or "0.00",  # always text
        "map_src": clean_map_src(raw_map),
    }


@login_required
def explore_spots(request):
    return render(request, 'tourism/explore_spots.html')


@login_required
def saved_spots(request):
    return render(request, 'tourism/saved_spots.html')


def reported_spots_albay_carousel(request):
    spots = []
    csv_path = os.path.join(settings.BASE_DIR, "shared", "static", "tourism_touristspot.csv")

    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("province", "").strip().lower() != "albay":
                continue
            if not row.get("id", "").strip() or not row.get("name", "").strip():
                continue
            spots.append(build_spot(row, "albay"))

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
    csv_path = os.path.join(settings.BASE_DIR, "shared", "static", "tourism_touristspot.csv")
    spot = None

    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # only check rows with province=albay
            if row.get("province", "").strip().lower() != "albay":
                continue

            # match the ID
            if row.get("id", "").strip() == str(spot_id):
                spot = build_spot(row, "albay")
                break

    if not spot:
        # If no spot is found, return a 404-like page
        return render(request, "404.html", status=404)

    # Pass the single spot to a new template
    return render(request, "tourism/reported_spots_albay_map.html", {"spot": spot})
