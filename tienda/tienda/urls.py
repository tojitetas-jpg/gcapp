
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

#views de cada app

from core import views as core_views
from usuarios import views as user_views
from productos import views as product_views
from pedidos import views as order_views

urlpatterns = [

    #Admin
    path('admin/', admin.site.urls),

    #Paginas principales (core)
    path("", core_views.home, name="home"),
    path("contact/", core_views.contact, name="contact"),
    path("about/", core_views.about, name="about"),
    path("services/", core_views.services, name="services"),

    #Productos
    path("all-products/", product_views.products, name="products"),
    path("product/<int:id>/", product_views.product, name="product"),

    #Usuarios
    path("login/", user_views.login_view, name="login"),
    path("register/", user_views.register_view, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),

]

