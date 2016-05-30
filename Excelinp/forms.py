from django import forms
from .models import Item
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

class searchForm(forms.Form):
	code2 = forms.CharField(required=True)

class customHaystackSearchForm(ModelSearchForm):
	code = forms.CharField(required=True, label="Item name or Code", 
							widget=forms.TextInput(attrs={'placeholder': 'eg: 18SSTT','class': 'validate','autofocus':'autofocus', 'required':'required'}))
