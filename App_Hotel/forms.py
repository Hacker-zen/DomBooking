from django import forms
from .models import Booking, Amenity, Amenity, Location, Room, Payment, Review

class FilterForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False)
    rating = forms.DecimalField(required=False, max_digits=3, decimal_places=2, widget=forms.NumberInput(attrs={'min': 0, 'max': 10}))
    amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Booking
        fields = ['guests_adult', 'guests_children', 'check_in_date', 'check_out_date', 'room']
        # exclude = ['user', 'total_guest']
        
    def __init__(self, *args, hotel=None, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['guests_adult'].initial = 0
        self.fields['guests_children'].initial = 0
        if hotel:
            self.fields['room'] = forms.ModelChoiceField(queryset=Room.objects.filter(hotel=hotel))

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'name_on_card', 'card_number', 'expire_month', 'expire_year', 'ccv']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].required = False

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'cash':
            self.fields['amount'].required = True
            if not cleaned_data.get('amount'):
                self.add_error('amount', 'Amount is required for cash payments.')
        elif payment_method == 'card':
            required_fields = ['name_on_card', 'card_number', 'expire_month', 'expire_year', 'ccv']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for card payments.')
        return cleaned_data
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} {'(highest)' if i == 5 else '(lowest)' if i == 1 else ''}") for i in range(5, 0, -1)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:130px;'}),
        }
        labels = {
            'rating': 'Rating *',
            'comment': 'Your Review *',
        }