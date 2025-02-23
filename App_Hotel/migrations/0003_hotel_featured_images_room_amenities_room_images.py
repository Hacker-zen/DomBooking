# Generated by Django 5.1 on 2024-10-29 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Hotel', '0002_alter_hotel_description_alter_hotel_price_per_night_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='featured_images',
            field=models.ImageField(blank=True, null=True, upload_to='featured/'),
        ),
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(to='App_Hotel.amenity'),
        ),
        migrations.AddField(
            model_name='room',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='rooms/'),
        ),
    ]
