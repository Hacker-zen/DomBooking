from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Booking, Room, Payment, Wishlist, Review
from .forms import BookingForm, FilterForm,PaymentForm, ReviewForm
from App_Auth.forms import CustomerProfileForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse

# ################ Home page ################
def home(request):
    user = request.user
    hotels = Hotel.objects.all() 
    return render(request, 'App_Hotel/Hotels/home.html', {'user': user, 'hotels': hotels})

# ################ About page ################
def about(request):
    return render(request, 'App_Hotel/Others/about.html')

# ################ Contact page ################
def contact(request):
    return render(request, 'App_Hotel/Others/contactus.html')

# ################ FAQ ################
def faq(request):
    return render(request, 'App_Hotel/Others/faq.html')

# ################ WishList ################

@login_required
def add_to_wishlist(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    profile = request.user.profile  

    # Add hotel to wishlist if it doesn't already exist
    wishlist_item, created = Wishlist.objects.get_or_create(user=profile, hotel=hotel)

    if created:
        message = "Hotel added to wishlist."
    else:
        message = "Hotel is already in your wishlist."

    return JsonResponse({'message': message, 'status': 'added' if created else 'exists'})

@login_required
def remove_from_wishlist(request, hotel_id):
    profile = request.user.profile 
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    # Try to get the wishlist item and delete it if it exists
    wishlist_item = Wishlist.objects.filter(user=profile, hotel=hotel).first()
    if wishlist_item:
        wishlist_item.delete()
        message = "Hotel removed from wishlist."
        status = "removed"
    else:
        message = "Hotel not found in your wishlist."
        status = "not_found"
    
    return JsonResponse({'message': message, 'status': status})

@login_required(login_url='App_Auth:signin')
def wishlist_view(request):
    # Get the wishlist items for the logged-in user's profile
    profile = request.user.profile
    wishlist_items = Wishlist.objects.filter(user=profile)

    return render(request, 'App_Hotel/Hotels/wishlist.html', {'wishlist_items': wishlist_items})

# ################ Review Section ################
@login_required(login_url='App_Auth:signup')
def submit_review(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    
    # Check if the user has already reviewed this hotel
    existing_review = hotel.reviews.filter(user=request.user.profile).first()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            if existing_review:
                # If an existing review is found, update it
                existing_review.rating = review_form.cleaned_data['rating']
                existing_review.comment = review_form.cleaned_data['comment']
                existing_review.save()
                message = "Your review has been updated."
            else:
                # If no review exists, create a new one
                review = review_form.save(commit=False)
                review.hotel = hotel
                review.user = request.user.profile
                review.save()
                message = "Your review has been submitted."

          
            return redirect('App_Hotel:hotel_detail', pk=pk)

    return redirect('App_Hotel:hotel_detail', pk=pk)

# View to handle liking a review
@login_required(login_url='App_Auth:signup')
def toggle_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user_profile = request.user.profile  # Assuming request.user.profile links to CustomerProfile

    if user_profile in review.likes.all():
        # User has already liked this review, so remove the like
        review.likes.remove(user_profile)
    else:
        # User has not liked this review yet, so add the like
        review.likes.add(user_profile)

    return redirect('App_Hotel:hotel_detail', pk=review.hotel.pk)

# ################  Blog page ################
# def blog(request):
#     return render(request, 'App_Hotel/Others/blog.html')

# ################ List hotels ################
def hotel_list(request):
    hotels = Hotel.objects.all()  
    filter_form = FilterForm(request.GET)  
    
    if filter_form.is_valid():
        location = filter_form.cleaned_data.get('location')
        rating = filter_form.cleaned_data.get('rating')
        amenities = filter_form.cleaned_data.get('amenities')
        
        if location:
            hotels = hotels.filter(location=location)
        if rating:
            hotels = hotels.filter(rating__gte=rating)  
        if amenities:
            hotels = hotels.filter(amenities__in=amenities).distinct()  

    return render(request, 'App_Hotel/Hotels/hotel_list.html', {'hotels': hotels, 'filter_form': filter_form})

# Hotel detail view
@login_required(login_url='App_Auth:signup')
def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    room_types = Room.objects.filter(hotel=hotel)
    reviews = hotel.reviews.all()

    existing_review = hotel.reviews.filter(user=request.user.profile).first()

    if request.method == 'POST':
        form = BookingForm(request.POST, hotel=hotel)  
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user.profile
            booking.total_guest = form.cleaned_data['guests_adult'] + form.cleaned_data['guests_children']
            booking.room = form.cleaned_data['room'] 

            booking.save()
            return redirect('App_Hotel:cart')
        else:
            print("Form errors:", form.errors)
            
    else:
        form = BookingForm(hotel=hotel)  

    review_form = ReviewForm()

    return render(request, 'App_Hotel/Hotels/hotel_detail.html', {
        'hotel': hotel,
        'room_types': room_types,
        'form': form,
        'reviews': reviews,
        'review_form': review_form,
    })

# @login_required
# def cart(request):
#     bookings = Booking.objects.filter(user=request.user.profile, is_confirmed=False, payment_status=False)
#     total_price = sum(booking.room.price_per_night for booking in bookings)

#     return render(request, 'App_Hotel/Bookings/cart.html', {
#         'bookings': bookings,
#         'total_price': total_price,
#     })

@login_required(login_url='App_Auth:signup')
def cart(request):
    bookings = Booking.objects.filter(user=request.user.profile, is_confirmed=False, payment_status=False)
    total_price = 0  

    for booking in bookings:
        stay_duration = (booking.check_out_date - booking.check_in_date).days
        room_price = booking.room.price_per_night * stay_duration
        booking.total_price = room_price 
        booking.stay_duration = stay_duration
        total_price += room_price

    # Paginate bookings
    paginator = Paginator(bookings, 10)  
    page_number = request.GET.get('page')
    page_bookings = paginator.get_page(page_number)

    return render(request, 'App_Hotel/Bookings/cart.html', {
        'bookings': page_bookings,
        'total_price': total_price,
    })

@login_required(login_url='App_Auth:signup')
def remove_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user.profile)
    booking.delete()
    messages.success(request, "Booking has been removed from your cart.")
    return redirect('App_Hotel:cart')

@login_required(login_url='App_Auth:signup')
@transaction.atomic 
def payment(request):
    bookings = Booking.objects.filter(user=request.user.profile, is_confirmed=False, payment_status=False)

    # Calculate total price and store stay duration for each booking
    total_price = 0
    for booking in bookings:
        stay_duration = (booking.check_out_date - booking.check_in_date).days
        booking.stay_duration = stay_duration 
        costing = booking.room.price_per_night
        booking.costing = costing
        booking.total_cost = stay_duration * costing
        total_price += booking.total_cost

    payment_form = PaymentForm(request.POST or None)
    user_details_form = CustomerProfileForm(instance=request.user.profile, user=request.user)

    if request.method == "POST" and payment_form.is_valid():
        payment = payment_form.save(commit=False)
        payment.amount = total_price
        payment.is_paid = True
        payment.save()
        payment.booking.set(bookings)  # Assign bookings to the payment
        bookings.update(is_confirmed=True, payment_status=True)

        return redirect('App_Hotel:payment_confirmation') 

    context = {
        'payment_form': payment_form,
        'user_details_form': user_details_form,
        'bookings': bookings,
        'total_price': total_price,
    }
    return render(request, 'App_Hotel/Bookings/payment.html', context)

@login_required
def payment_confirmation(request):
    return render(request, 'App_Hotel/Bookings/payment_confirmation.html')

@login_required
def payments_list(request):
    payments = Payment.objects.filter(booking__user=request.user.profile).distinct()
    return render(request, 'App_Hotel/Bookings/payment_list.html', {'payments': payments})



