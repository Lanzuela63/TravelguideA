from django.shortcuts import render

def webar_view(request, spot_id=None):
    context = {'spot_id': spot_id}
    return render(request, 'ar/webar_scene.html', context)

def location_ar_view(request):
    # For now, just pass some dummy data
    context = {
        'message': 'Location AR View - Backend is working!',
        'latitude': 0.0,
        'longitude': 0.0,
    }
    return render(request, 'ar/location_ar_scene.html', context)
