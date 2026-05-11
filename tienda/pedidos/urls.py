from django.urls import path
from . import views

urlpatterns = [
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("carrito/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("checkout/", views.checkout, name="checkout"),
    path("confirmacion/", views.order_confirmation, name="order_confirmation"),

    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),
]

