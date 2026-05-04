from django.shortcuts import render, get_object_or_404
from .models import Product

def products(request):
    products = Product.objects.all()
    return render(request, "all products.html", {"products": products})

def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product.html", {"product": product})

def categories(request):
    return render(request, 'categories.html')