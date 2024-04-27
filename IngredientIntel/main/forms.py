from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
import cv2
from pyzbar.pyzbar import decode
from dal import autocomplete


class SearchForm(forms.Form):
    model = forms.ChoiceField(choices=[('Product', 'Product'), ('Ingredient', 'Ingredient'), ('Company', 'Company')], required=True, label="")
    query = forms.CharField(label="", required=True)

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['flagged_ingredients', 'color_mode']
        widgets = {
            'flagged_ingredients': autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete'),
        }

class BarcodeForm(forms.Form):
    #name = forms.CharField(widget=forms.TextInput(attrs={'class':'centerform'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'centerform'}))
    image.help_text = None

class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'date_founded', 'notes', 'company_registration_number', 'company_address']
        widgets = { 
            'name': forms.TextInput(attrs={'class':'centerform'}),
            'date_founded': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                        'placeholder': 'Select a date',
                        'type': 'date'
              }),
            'notes': forms.TextInput(attrs={'class':'centerform'}),
            'company_registration_number': forms.TextInput(attrs={'class':'centerform'}),
            'company_address': forms.TextInput(attrs={'class':'centerform'}),
        }


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['ingredients', 'name', 'warnings', 'notes', 'item_id']
        widgets = {
            'ingredients': autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete'),
        }

class ConsumerCreationForm(UserCreationForm):
    # error_css_class = 'alert alert-danger'
    # required_css_class = 'invalid-tooltip'
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'centerform'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'centerform'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(ConsumerCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'centerform'
        self.fields['password1'].widget.attrs['class'] = 'centerform'
        self.fields['password2'].widget.attrs['class'] = 'centerform'

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class ResearcherSignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'centerform'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'centerform'}))
    email = forms.EmailField(max_length=128, widget=forms.EmailInput()) 

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2','email')
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(ResearcherSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'centerform'
        self.fields['password1'].widget.attrs['class'] = 'centerform'
        self.fields['password2'].widget.attrs['class'] = 'centerform'
        self.fields['email'].widget.attrs['class'] = 'centerform'

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class SCInoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        researcher = kwargs.pop('researcher')
        super().__init__(*args, **kwargs)

        self.fields['researcher'].initial = researcher # sets producing company on initialization

    class Meta:
        model = SCINote
        fields = ('__all__')
        widgets = {
            'ingredient': autocomplete.ModelSelect2(url='ingredient-autocomplete'),
            'researcher': forms.HiddenInput()
        }