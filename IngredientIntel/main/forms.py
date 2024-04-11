from django import forms

class SearchForm(forms.Form):
    model = forms.ChoiceField(choices=[('Ingredient', 'Ingredient'), ('Product', 'Product'), ('Company', 'Company')], required=True, label="")
    query = forms.CharField(label="", required=True)

class SettingsForm(forms.Form):
    display_mode = forms.ChoiceField(choices=[("light", "Light"), ("dark", "Dark")], required=True, label="Color Modes:")
    diet_mode = forms.ChoiceField(choices=[(" ", " "),("no restrictions", "No Restrictions"),("vegetarion", "Vegetarian"),("vegan", "Vegan"),("pescatarion", "Pescartarian")], required=True, label="Hide Items:")
    new_name = forms.CharField(required=False, label="Name Changer:")

class BarcodeForm(forms.Form):
    query = forms.ImageField()

