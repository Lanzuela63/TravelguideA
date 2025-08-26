#apps/tourism/views/api_views.py
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.tourism.models import TouristSpot
from apps.tourism.serializers import TouristSpotSerializer


class TouristSpotListAPIView(generics.ListAPIView):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer

@api_view(["GET"])
def list_tourist_spots(request):
    spots = TouristSpot.objects.all()
    serializer = TouristSpotSerializer(spots, many=True, context={"request": request})
    return Response(serializer.data)
