from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^basket_adding/$', views.basket_adding, name='basket_adding'),
    url(r"^basket_update/$", views.basket_update, name="basket_update"),
    url(r"^basket_del/$", views.basket_del, name="basket_del"),
    url(r"^basket_del_all/$", views.basket_del_all, name="basket_del_all"),
    url(r'^checkout/$', views.checkout, name="checkout"),
    url(r'^order_create/$', views.PrepareOrder.as_view(), name="prepare_order"),
]