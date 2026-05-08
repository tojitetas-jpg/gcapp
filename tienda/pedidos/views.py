from django.shortcuts import render, redirect
from .cart import Cart

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('ver_carrito')

def ver_carrito(request):
    cart = Cart(request)
    return render(request, 'carrito.html', {'cart': cart})
