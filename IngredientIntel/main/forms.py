from django import forms

class SearchForm(forms.Form):
    search_criteria = forms.ChoiceField(choices=[('ingredient', 'Ingredient'), ('product', 'Product'), ('company', 'Company')], required=True, label="")
    search_query = forms.CharField(label="", required=True)