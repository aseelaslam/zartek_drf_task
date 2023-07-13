
from celery import shared_task
from .models import Ride

@shared_task
def update_ride_location(ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)

        ride.current_location = "New location"
        ride.save()
    except Ride.DoesNotExist:
        pass
