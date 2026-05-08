from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm


def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    # Obtener filtros desde la URL
    search = request.GET.get("search")
    condition = request.GET.get("condition")
    category = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # FILTRO POR BÚSQUEDA
    if search:
        products = products.filter(name__icontains=search)

    # FILTRO POR ESTADO
    if condition:
        products = products.filter(condition=condition)

    # FILTRO POR CATEGORÍA
    if category:
        products = products.filter(category__id=category)

    # FILTRO POR PRECIO MÍNIMO
    if min_price:
        products = products.filter(price__gte=min_price)

    # FILTRO POR PRECIO MÁXIMO
        products = products.filter(price__lte=max_price)

    
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
        product = Product.objects.create(
            name=request.POST.get("title"),
            price=request.POST.get("price"),
            description=request.POST.get("description"),
            details=request.POST.get("details"),
            image=request.FILES.get("image"),
            category=Category.objects.get(id=request.POST.get("category")),
            condition=request.POST.get("condition"),

        )

        product.user = request.user
        product.save()

        return redirect("home")

    categorias = Category.objects.all()
    return render(request, "publicar_producto.html", {"categories": categorias})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect("products")  # te lleva a all-products

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product", id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {
        "form": form,
        "product": product
    })


