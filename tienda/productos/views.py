from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "all products.html", {
        "products": products,
        "categories": categories
    })

def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product.html", {"product": product})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, 'category_products.html', {

        'category': category,
        'products': products,
        'categories': categories

    })

#hola