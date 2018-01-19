from django.conf.urls import url, include
from django.contrib import admin
from products import views

urlpatterns = [
    # url(r'^landing123/', views.landing, name='landing'),
    url(r'^product/flower/(?P<product_id>\d+)$', views.product, name='product'),
]
