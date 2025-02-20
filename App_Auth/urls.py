from django.urls import path
from . import views

app_name = 'App_Auth'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('404/', views.handle_not_found, name='404'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', views.profile_update, name='profile_update'),

    path('admin-login/', views.admin_login_view, name='admin-login'),
    path('logout/', views.admin_logout_view, name='admin-logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('locations/', views.location_list, name='location_list'),
    path('locations/add/', views.add_location, name='add_location'),
    
    path('amenity/', views.amenity_list, name='amenity_list'),
    path('amenities/add/', views.add_amenity, name='add_amenity'),
    
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/add/', views.add_hotel, name='add_hotel'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'), 
    
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),

    path('payments/', views.payment_list, name='payment_list'),
    path('payments/view/<int:pk>/', views.view_payment, name='view_payment'), 
    path('payments/update/<int:pk>/', views.update_payment, name='update_payment'),

    path('all-profiles/', views.view_profiles, name='profiles'),
]


