from django.conf.urls import url
from .views import *
from shop.templates import *

urlpatterns = [
    url(r'^shop/$', index, name="index"),
]