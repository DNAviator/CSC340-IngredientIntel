from django import forms

class SearchForm(forms.Form):
    search_criteria = forms.ChoiceField(choices=[('ingredient', 'Ingredient'), ('product', 'Product'), ('company', 'Company')], required=True, label="")
    search_query = forms.CharField(label="", required=True)

class SettingsForm(forms.Form):

    display_mode = forms.ChoiceField(choices=[("light", "Light"), ("dark", "Dark")], required=True, label="Display Mode:")
    hidden_items = forms.CharField(required=True, label="Hide Items:")
