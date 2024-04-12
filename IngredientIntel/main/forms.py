from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    model = forms.ChoiceField(choices=[('Ingredient', 'Ingredient'), ('Product', 'Product'), ('Company', 'Company')], required=True, label="")
    query = forms.CharField(label="", required=True)

class SettingsForm(forms.Form):
    display_mode = forms.ChoiceField(choices=[("light", "Light"), ("dark", "Dark")], required=True, label="Color Modes:")
    diet_mode = forms.ChoiceField(choices=[(" ", " "),("no restrictions", "No Restrictions"),("vegetarion", "Vegetarian"),("vegan", "Vegan"),("pescatarion", "Pescartarian")], required=True, label="Hide Items:")
    new_name = forms.CharField(required=False, label="Name Changer:")

class BarcodeForm(forms.Form):
    query = forms.ImageField()

class ConsumerCreationForm(UserCreationForm):
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


class CompanyCreationForm(UserCreationForm):
    """
    *** Not Completed ***
    Form used to create Companies
    Takes:
        Buisness Registration Number (9 digits)
        Registered Buisness Address
        Primary Buisness Contact:
            First_name
            Last_name
            Email
        Company_Name
    """
    email = forms.EmailField()
    company_registration_number = forms.CharField(max_length=9)
    
    class Meta:
        model = User
        fields = ('password1', 'password2')
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CompanyCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None