from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from App_Auth.models import CustomerProfile
from django.utils import timezone
from Core.settings import EMAIL_HOST_USER, AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator

# class User(AbstractUser):
#     is_customer = models.BooleanField(default=True)

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(null=True, blank=True, upload_to='icons/')

    def __str__(self):
        return self.name
    
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='hotels')
    description = models.TextField(null=True, blank=True)
    amenities = models.ManyToManyField(Amenity)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    images = models.ImageField(upload_to='hotels/')
    featured_images = models.ImageField(null=True, blank=True, upload_to='featured/')
    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100, null=True, blank=True)
    amenities = models.ManyToManyField(Amenity)
    number_of_beds = models.IntegerField(null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    images = models.ImageField(null=True, blank=True, upload_to='rooms/')

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name}"

class Booking(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests_adult = models.IntegerField()
    guests_children = models.IntegerField()
    total_guest = models.IntegerField()
    is_confirmed = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking {self.id} by {self.user.user.email}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
    ]

    booking = models.ManyToManyField(Booking, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    name_on_card = models.CharField(max_length=100,blank=True, null=True)
    card_number = models.CharField(max_length=16,blank=True, null=True)
    expire_month = models.CharField(max_length=2,blank=True, null=True)
    expire_year = models.CharField(max_length=4,blank=True, null=True)
    ccv = models.CharField(max_length=4,blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} for Bookings: {', '.join(str(b.id) for b in self.booking.all())}"

# Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='wishlist')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hotel')  

    def __str__(self):
        return f"{self.user} - {self.hotel.name}"

# Review Section 
class Review(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='reviews')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    likes = models.ManyToManyField(CustomerProfile, related_name="liked_reviews", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hotel')  # One review per user per hotel

    def __str__(self):
        return f"{self.user.user.email} - {self.hotel.name} - {self.rating} Stars"



        