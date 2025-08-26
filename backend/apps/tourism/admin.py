from django.contrib import admin
from .models import TouristSpot, Category, Location, Review, Gallery, OperatingHour

@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_featured', 'location', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tourist_spot', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'tourist_spot__name')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('tourist_spot', 'image', 'caption')
    search_fields = ('caption',)

@admin.register(OperatingHour)
class OperatingHourAdmin(admin.ModelAdmin):
    list_display = ('tourist_spot', 'day_of_week', 'open_time', 'close_time')
    list_filter = ('day_of_week',)

# Optional: Customize Admin Site Branding
admin.site.site_header = "Bicol Travel Guide Admin"
admin.site.site_title = "Bicol Travel CMS"
admin.site.index_title = "Welcome to the Bicol Travel Admin Portal"
