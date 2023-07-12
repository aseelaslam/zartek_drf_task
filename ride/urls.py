from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('rides/', RideListCreateView.as_view(), name='ride-list-create'),
    path('rides/<int:pk>/', RideRetrieveView.as_view(), name='ride-retrieve'),
    path('rides/<int:pk>/update-status/', RideStatusUpdateView.as_view(), name='ride-update-status'),
    path('rides/accept/', AcceptRideView.as_view(), name='accept-ride'),

]
