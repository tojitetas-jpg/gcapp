from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# IMPORTA TUS PRODUCTOS
from productos.models import Product   # ← Ajusta si tu modelo se llama distinto


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

        print("EMAIL RECIBIDO:", email)
        print("PASSWORD RECIBIDO:", password)

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
#   PERFIL TIPO INSTAGRAM
# -----------------------------
@login_required
def profile_view(request):
    productos = Product.objects.filter(user=request.user)

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'products': productos
    })

@login_required
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Guardar foto si se sube
        if "photo" in request.FILES:
            profile.photo = request.FILES["photo"]
            profile.save()

        # Guardar datos del usuario
        user = request.user
        user.username = username
        user.email = email
        user.save()

        return redirect("profile")

    return render(request, "accounts/edit_profile.html", {
        "user": request.user,
        "profile": profile
    })
