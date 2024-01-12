from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='front-home'),
    path('recommended', views.recommended, name='front-recommended'),
    path('cart', views.cart, name='front-cart'),
    path('sell', views.sell, name='front-sell'),
    re_path(r'products/*', views.product, name='front-product'),
]
