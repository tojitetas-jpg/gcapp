from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Product
from .cart import Cart
from .models import Order, OrderItem

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect(request.META.get("HTTP_REFERER", "/"))


def ver_carrito(request):
    cart = Cart(request)
    return render(request, "carrito.html", {"cart": cart})

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect(request.META.get("HTTP_REFERER", "/"))


def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            postal_code=request.POST.get("postal_code"),
            total=cart.get_total(),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

        cart.clear()
        return redirect("order_confirmation", order_id=order.id)

    return render(request, "checkout.html", {"cart": cart})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_confirmation.html", {"order": order})

def mis_pedidos(request):
    pedidos = Order.objects.filter(user=request.user)
    return render(request, "mis_pedidos.html", {"pedidos": pedidos})
