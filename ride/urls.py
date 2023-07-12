from django.urls import path
from .views import UserRegistrationView, UserLoginView,RideListCreateView,RideRetrieveView

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('rides/', RideListCreateView.as_view(), name='ride-list-create'),
    path('rides/<int:pk>/', RideRetrieveView.as_view(), name='ride-retrieve'),
]
