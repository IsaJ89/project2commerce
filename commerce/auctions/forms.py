from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)