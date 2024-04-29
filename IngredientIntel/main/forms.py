from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
import cv2
from pyzbar.pyzbar import decode
from dal import autocomplete


class SearchForm(forms.Form):
    """
    Form takes user input for either product, company, or ingredient, which is used to find an item of a similar name. 
    """
    model = forms.ChoiceField(choices=[('Product', 'Product'), ('Ingredient', 'Ingredient'), ('Company', 'Company')], required=True, label="", widget=forms.Select(attrs={'class':'form-select', "style":"width-max:auto;"}))
    query = forms.CharField(label="search...", required=True, widget=forms.TextInput(attrs={'placeholder':"Search...", 'class':'form-control', 'type':'text'}))

class SettingsForm(forms.ModelForm):
    """
    Form shows a users personal settings
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['color_mode'].widget.attrs['class'] = 'form-select'
    class Meta:
        model = Profile
        fields = ['flagged_ingredients', 'color_mode']
        widgets = {
            'flagged_ingredients': autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete'),
            }
        
        

class BarcodeForm(forms.Form):
    """
    Form that takes image from a user for barcode scanning
    """
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'centerform'}))
    image.help_text = None

class NewCompanyForm(forms.ModelForm):
    """
    Form takes parameters to create a new company
    """
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
    """
    Form takes a companies input to create a new product
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(NewProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['warnings'].widget.attrs['class'] = 'form-control'
        self.fields['notes'].widget.attrs['class'] = 'form-control'
        self.fields['item_id'].widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Product
        fields = ['ingredients', 'name', 'warnings', 'notes', 'item_id']
        widgets = {
            'ingredients': autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete'),
        }

class ConsumerCreationForm(UserCreationForm):
    """
    Form allows the creation of new users for our web app
    """
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
    """
    Form allows the creation of new researchers
    """
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
    """
    Form allows a researcher to add a science note to a corresponding ingredient 
    """
    def __init__(self, *args, **kwargs):
        researcher = kwargs.pop('researcher')
        super(SCInoteForm, self).__init__(*args, **kwargs)
        self.fields['researcher'].initial = researcher # sets producing company on initialization
        self.fields['research_credits'].widget.attrs['class'] = 'form-control'
        self.fields['notes_content'].widget.attrs['class'] = 'form-control'
        self.fields['citations'].widget.attrs['class'] = 'form-control'
        
    class Meta:
        model = SCINote
        fields = ( 'ingredient', 'research_credits', 'notes_content', 'citations', 'researcher')
        widgets = {
            'ingredient': autocomplete.ModelSelect2(url='ingredient-autocomplete'),
            'researcher': forms.HiddenInput()
        }

class ApiForm(forms.ModelForm):
    print()