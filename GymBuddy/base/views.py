from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def paginaLogin(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        try:
            user = User.objects.get(username = usuario)
        except:
            messages.error(request, 'Usuario não encontrado')
        aut = authenticate(request, username=usuario, password=senha)
        if aut is not None:
            login(request, aut)
            return redirect("home")
        
    context = {}
    return render(request, 'criar-login.html', context)

def logoutUsuario(request):
    logout(request)
    return redirect("home")

def home(request):
    return render(request, 'home.html')