from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import generics, permissions,status,generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User,Ride
from .serializers import UserRegistrationSerializer, UserLoginSerializer,RideSerializer,RideStatusSerializer
from rest_framework.views import APIView

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .tasks import update_ride_location

from rest_framework.permissions import IsAuthenticated

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient


 


# Create your views here.


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})





class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class RideListCreateView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class RideRetrieveView(generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer





class RideStatusUpdateView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideStatusSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {'status': request.data.get('status')}
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)




def start_ride_tracking(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    update_ride_location.apply_async(args=[ride_id], countdown=5)
    return HttpResponse("Ride tracking started")



class AcceptRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        driver = request.user  
        ride_id = request.data.get('ride_id')

        try:
            ride = Ride.objects.get(id=ride_id, driver=None)  
        except Ride.DoesNotExist:
            return Response({'message': 'Ride not found or already assigned to a driver'}, status=400)
        




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
        url = reverse('ride-list')
        response = client.get(url)
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
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
       