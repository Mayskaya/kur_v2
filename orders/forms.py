from django import forms
from .models import *


class CheckoutContactForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=["name_customer", "phone_customer","email_customer","address_customer","comments", "total_price"]
        labels={
            "name_customer" : "Имя",
            "phone_customer" : "Телефон",
            "email_customer" : "E-mail",
            "address_customer" : "Адрес",
            'comments' : "Комментарии к заказу"
        }