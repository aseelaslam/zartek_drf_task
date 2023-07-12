from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Ride

class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'pickup_location', 'dropoff_location', 'status', 'created_at', 'updated_at')

class RideAdminInline(admin.StackedInline):
    model = Ride
    extra = 0
    fk_name = 'rider'

class CustomUserAdmin(UserAdmin):
    inlines = [RideAdminInline]


admin.site.unregister(User)


admin.site.register(User, CustomUserAdmin)

admin.site.register(Ride, RideAdmin)
