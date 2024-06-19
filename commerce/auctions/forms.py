from django import forms
from django.forms import ModelForm

from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name','description','initial_bid','photo','category']
    
    photo = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': "Add a link to your product's image"}))