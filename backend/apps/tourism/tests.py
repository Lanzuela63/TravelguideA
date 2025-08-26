# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.tourism.models import TouristSpot, Location, Category


class TouristSpotAPITestCase(TestCase):
    def setUp(self):
        # Create test data
        location = Location.objects.create(name="Test Location")
        category = Category.objects.create(name="Test Category")
        TouristSpot.objects.create(
            name="Test Spot 1",
            description="A beautiful place.",
            location=location,
            category=category
        )
        TouristSpot.objects.create(
            name="Test Spot 2",
            description="Another beautiful place.",
            location=location,
            category=category
        )
        self.client = APIClient()

    def test_get_tourist_spots(self):
        # Send GET request to the endpoint
        response = self.client.get('/api/tourist-spots/')

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "Test Spot 1")
        self.assertEqual(response.data[1]['name'], "Test Spot 2")