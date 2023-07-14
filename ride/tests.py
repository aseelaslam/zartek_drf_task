from .models import Ride
from .serializers import RideSerializer
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.
class RideModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.ride = Ride.objects.create(rider=self.user1, pickup_location='Location 1', dropoff_location='Location 2')

    def test_ride_creation(self):
        ride = Ride.objects.get(id=self.ride.id)
        self.assertEqual(ride.rider, self.user1)
        self.assertEqual(ride.pickup_location, 'Location 1')
        self.assertEqual(ride.dropoff_location, 'Location 2')
        self.assertIsNone(ride.driver)

    def test_ride_list_api(self):
        client = APIClient()
        url = reverse('ride-retrieve', args=[self.ride.id])
        response = client.get(url)
        ride = Ride.objects.get(id=self.ride.id)
        serializer = RideSerializer(ride)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)



class AcceptRideAPITestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.ride = Ride.objects.create(rider=self.user1, pickup_location='Location 1', dropoff_location='Location 2')

    def test_accept_ride_api(self):
        client = APIClient()
        url = reverse('accept-ride')
        data = {'ride_id': self.ride.id}
        client.force_authenticate(user=self.user2)  # Authenticate as a driver
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Ride accepted successfully')
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.driver, self.user2)