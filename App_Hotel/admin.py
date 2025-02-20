from django.contrib import admin

# Register your models here.
from App_Hotel import models


admin.site.register(models.Location)
admin.site.register(models.Amenity)
admin.site.register(models.Hotel)
admin.site.register(models.Room)
admin.site.register(models.Booking)
admin.site.register(models.Payment)
admin.site.register(models.Wishlist)
