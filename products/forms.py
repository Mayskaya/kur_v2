# from django import forms
from django.forms import ModelForm
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name_product', 'description_product','price', 'is_active', 'created', 'updated']