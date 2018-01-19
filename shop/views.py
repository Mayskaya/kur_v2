from django.shortcuts import render
from products.models import *

def index(request):
    productsIMG = ProductIMG.objects.filter(is_active=True , product__is_active=True)
    productsIMG_rose = productsIMG.filter(product__category__id=1)
    productsIMG_other = productsIMG.filter(product__category__id=2)
    return render(request, "shop/index.html", locals())
