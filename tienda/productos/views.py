from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.shortcuts import render, redirect
from .models import Product

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

def publicar_producto(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("title"),
            price=request.POST.get("price"),
            description=request.POST.get("description"),
            details=request.POST.get("details"),
            image=request.FILES.get("image"),
            category=Category.objects.get(id=request.POST.get("category")),
        )
        return redirect("home")

    categorias = Category.objects.all()
    return render(request, "publicar_producto.html", {"categories": categorias})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect("products")  # te lleva a all-products

