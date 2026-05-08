from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
