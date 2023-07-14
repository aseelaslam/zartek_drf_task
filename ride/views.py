from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import generics, permissions,status,generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User,Ride
from .serializers import UserRegistrationSerializer, UserLoginSerializer,RideSerializer,RideStatusSerializer
from rest_framework.views import APIView



from .tasks import update_ride_location



from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import requests







 


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
    def post(self, request):
        ride_id = request.data.get('ride_id')
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

        ride.driver = request.user  # Assuming authenticated user is the driver
        ride.save()
        return Response({'message': 'Ride accepted successfully'}, status=status.HTTP_200_OK)



        





