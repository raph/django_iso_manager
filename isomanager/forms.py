# from dal import autocomplete
# from django import forms
# from .models import CatalogItem, OsEdition
#
#
# class CatalogItemForm(forms.ModelForm):
#     os_edition = forms.ModelChoiceField(
#         queryset=OsEdition.objects.all(),
#         widget=autocomplete.ModelSelect2(url='os-autocomplete')
#     )
#
#     class Meta:
#         model = CatalogItem
#         fields = '__all__'
