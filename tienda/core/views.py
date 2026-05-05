from django.shortcuts import render
from productos.models import Product 

def home(request):
    popular_products = Product.objects.filter(popular=True)[:3]
    best_price_products = Product.objects.filter(best_price=True)[:3]
    return render(request, 'home.html', {

        'popular_products': popular_products,
        'best_price_products': best_price_products,

    })
   
def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

