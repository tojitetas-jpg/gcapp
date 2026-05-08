from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


# views de cada app
from core import views as core_views
from usuarios import views as user_views
from productos import views as product_views
from pedidos import views as order_views

urlpatterns = [

    # Admin
    path('admin/', admin.site.urls),

    # Paginas principales (core)
    path("", core_views.home, name="home"),
    path("contact/", core_views.contact, name="contact"),
    path("about/", core_views.about, name="about"),
    path("services/", core_views.services, name="services"),

    # Productos
    path("all-products/", product_views.products, name="products"),
    path("product/<int:id>/", product_views.product, name="product"),
    path('categorias/<slug:slug>/', product_views.category_products, name='category_products'),

    # Usuarios
    path("login/", user_views.login_view, name="login"),
    path("register/", user_views.register_view, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),

    #pedidos.
    path('pedidos/', include('pedidos.urls')),
]

# imagenes categorias
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
