from rest_framework import serializers
from .models import TouristSpot, Category, Location, Review, Gallery, OperatingHour, TourismReportedSpotAlbay


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class TouristSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristSpot
        fields = ['id', 'name', 'description', 'image', 'location']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class OperatingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHour
        fields = '__all__'


# Optional: For nested detail view
class TouristSpotDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, source='review_set', read_only=True)
    gallery = GallerySerializer(many=True, source='gallery_set', read_only=True)
    operatinghour = OperatingHourSerializer(read_only=True)

    class Meta:
        model = TouristSpot
        fields = '__all__'


# --- Serializer for TourismReportedSpot (CSV-backed model) ---
class TourismReportedSpotSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TourismReportedSpotAlbay
        fields = ['id', 'name', 'description', 'image', 'rating', 'image_url']

    def get_image_url(self, obj):
        return obj.image_url
