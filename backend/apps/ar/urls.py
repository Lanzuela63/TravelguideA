from django.urls import path
from .models import ARScene
from .views import nearby_ar_scenes, api_views, webar_view, location_ar_view
from .views.api_views import list_ar_scenes

app_name = 'ar'

urlpatterns = [
    path('api/scenes/nearby/', api_views.nearby_ar_scenes, name='nearby_ar_scenes'),
    path("api/scenes/", api_views.list_ar_scenes, name="list_scenes"),
    path('webar/<int:spot_id>/', webar_view, name='webar_scene'),
    path('webar/', webar_view, name='webar_scene_no_id'),
    path('location/', location_ar_view, name='location_ar_scene'),
]