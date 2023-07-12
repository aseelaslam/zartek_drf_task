from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('rides/', RideListCreateView.as_view(), name='ride-list-create'),
    path('rides/<int:pk>/', RideRetrieveView.as_view(), name='ride-retrieve'),
    path('rides/<int:pk>/start/', RideStartView.as_view(), name='ride-start'),
    path('rides/<int:pk>/complete/', RideCompleteView.as_view(), name='ride-complete'),
    path('rides/<int:pk>/cancel/', RideCancelView.as_view(), name='ride-cancel'),

]
