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
        # Guardar datos del formulario en la sesión
        request.session["checkout_data"] = {
            "full_name": request.POST.get("full_name"),
            "email": request.POST.get("email"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "postal_code": request.POST.get("postal_code"),
        }
        return redirect("order_confirmation")

    return render(request, "checkout.html", {"cart": cart})

def order_confirmation(request):
    cart = Cart(request)
    checkout_data = request.session.get("checkout_data")

    if not checkout_data:
        return redirect("checkout")

    # Si el usuario confirma el pedido
    if request.method == "POST":
        # Crear pedido
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=checkout_data["full_name"],
            email=checkout_data["email"],
            address=checkout_data["address"],
            city=checkout_data["city"],
            postal_code=checkout_data["postal_code"],
            total=cart.get_total(),
        )

        # Guardar productos
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

        # Vaciar carrito
        cart.clear()

        # Borrar datos del checkout
        del request.session["checkout_data"]

        # Mostrar pantalla de compra completada (MISMA PANTALLA)
        return render(request, "order_confirmation.html", {
            "order_completed": True,
            "order": order,
        })

    # Primera vez que se entra a order_confirmation
    return render(request, "order_confirmation.html", {
        "order_completed": False,
        "order": checkout_data,
        "cart": cart,
        "cart_total": cart.get_total(),
    })

    

def mis_pedidos(request):
    pedidos = Order.objects.filter(user=request.user)
    return render(request, "mis_pedidos.html", {"pedidos": pedidos})
