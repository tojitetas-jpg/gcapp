from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Modelos
from productos.models import Product
from pedidos.models import Order
from accounts.models import Profile


# -----------------------------
#   REGISTRO
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Ese nombre de usuario ya existe'})

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Ese email ya está registrado'})

        user = User.objects.create_user(username=username, email=email, password=password)

        # Crear perfil automáticamente
        Profile.objects.create(user=user)

        login(request, user)
        return redirect('home')

    return render(request, 'accounts/register.html')


# -----------------------------
#   LOGIN CON EMAIL
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'Email no encontrado'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Contraseña incorrecta'})

    return render(request, 'accounts/login.html')


# -----------------------------
#   LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------------
#   PERFIL
# -----------------------------
@login_required
def profile_view(request):

    # 🔥 FIX DEFINITIVO: crear perfil si no existe
    profile, created = Profile.objects.get_or_create(user=request.user)

    productos = Product.objects.filter(user=request.user)
    pedidos = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile': profile,
        'products': productos,
        'pedidos': pedidos,
    })


# -----------------------------
#   EDITAR PERFIL
# -----------------------------
@login_required
def edit_profile_view(request):

    # 🔥 FIX: asegurar que el perfil existe
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        # Actualizar datos del usuario
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Actualizar bio
        profile.bio = request.POST.get("bio")

        # Guardar foto si se subió
        if "photo" in request.FILES:
            profile.photo = request.FILES["photo"]

        profile.save()

        return redirect("profile")

    return render(request, "accounts/edit_profile.html", {
        "user": request.user,
        "profile": profile
    })
