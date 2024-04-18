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

class SettingsForm(forms.Form):
    display_mode = forms.ChoiceField(choices=[("light", "Light"), ("dark", "Dark")], required=True, label="Color Modes:")
    diet_mode = forms.ChoiceField(choices=[(" ", " "),("no restrictions", "No Restrictions"),("vegetarion", "Vegetarian"),("vegan", "Vegan"),("pescatarion", "Pescartarian")], required=True, label="Hide Items:")
    new_name = forms.CharField(required=False, label="Name Changer:")

class BarcodeForm(forms.Form):
    #name = forms.CharField(widget=forms.TextInput(attrs={'class':'centerform'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'centerform'}))
    image.help_text = None

class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('__all__')
        widgets = { 
            'products': forms.HiddenInput(),
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
#     def __init__(self, *args, **kwargs):
#         parent_company = kwargs.pop('producing_company')
#         super().__init__(*args, **kwargs)

#         self.fields['producing_company'].initial = Company.objects.get(name="Planters") #**** THIS NEEDS TO BE FIXED PROBABLY user.company   Set initial value based on user's company

    class Meta:
        model = Product
        fields = ('__all__')
        widgets = {
            'ingredients': autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete'),
            'producing_company': forms.HiddenInput()
        }

class ConsumerCreationForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'
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

        # for fieldname in ['username', 'password1', 'password2']:
        #     self.fields[fieldname].help_text = None

class CompanySelectionForm(forms.ModelForm):
    print()
    #companies = autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete'),
    #for items in Company.objects :
        #Company.registered_users.
    companies = forms.ChoiceField()



