from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewcart, name="cart"),
    path('add_cart/<str:food_type>/<int:food_id>/',
         views.add_cart, name='add_cart'),
    path('remove_cart_item/<str:food_type>/<int:food_id>/',
         views.remove_cart_item, name='remove_cart_item'),

]
