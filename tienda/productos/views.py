from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from .forms import ProductForm
from django.db.models import Q


# -----------------------------------------
#   HOME (para sliders Netflix)
# -----------------------------------------
def home(request):
    # Productos populares (marcados en la BD)
    popular_products = Product.objects.filter(is_popular=True)[:10]

    # Mejores precios (los más baratos)
    best_price_products = Product.objects.order_by('price')[:10]

    return render(request, "home.html", {
        "popular_products": popular_products,
        "best_price_products": best_price_products,
    })


# -----------------------------------------
#   TODOS LOS PRODUCTOS + FILTROS
# -----------------------------------------
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
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, "all_products.html", {
        "products": products,
        "categories": categories
    })


# -----------------------------------------
#   PRODUCTO INDIVIDUAL
# -----------------------------------------
def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product.html", {"product": product})


# -----------------------------------------
#   PRODUCTOS POR CATEGORÍA + FILTROS
# -----------------------------------------
def category_products(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)

    search = request.GET.get("search") or ""
    condition = request.GET.get("condition") or ""
    min_price = request.GET.get("min_price") or ""
    max_price = request.GET.get("max_price") or ""

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if condition:
        products = products.filter(condition=condition)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, "category_products.html", {
        "category": category,
        "products": products,
    })


# -----------------------------------------
#   PUBLICAR PRODUCTO
# -----------------------------------------
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


# -----------------------------------------
#   ELIMINAR PRODUCTO
# -----------------------------------------
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect("products")


# -----------------------------------------
#   EDITAR PRODUCTO
# -----------------------------------------
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
