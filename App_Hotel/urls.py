from django.urls import path
from . import views

app_name = 'App_Hotel'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    # path('blog/', views.home, name='home'),

    path('findhotels/', views.hotel_list, name='hotel_list'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),

    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:booking_id>/', views.remove_booking, name='remove_booking'),

    path('payment/', views.payment, name='payment'),
    path('payment/confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('payment-list/', views.payments_list, name='payments_list'),

    path('wishlist/add/<int:hotel_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:hotel_id>/', views.remove_from_wishlist, name='remove_from_wishlist'), 
    path('wishlist/', views.wishlist_view, name='wishlist'),

    path('hotel/<int:pk>/submit_review/', views.submit_review, name='submit_review'),
    path('hotel/<int:review_id>/toggle_like/', views.toggle_like, name='toggle_like'),

]
