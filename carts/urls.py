
from django.urls import path
from . import views

urlpatterns = [

    path('', views.cart, name='cart'),

    path(
        'add/<int:product_id>/',
        views.add_cart,
        name='add_cart'
    ),

    path(
        'increment/<int:item_id>/',
        views.increment_cart,
        name='increment_cart'
    ),

    path(
        'decrement/<int:item_id>/',
        views.decrement_cart,
        name='decrement_cart'
    ),

    path(
        'update/<int:item_id>/',
        views.update_cart,
        name='update_cart'
    ),

    path(
        'remove/<int:item_id>/',
        views.remove_cart,
        name='remove_cart'
    ),

]
