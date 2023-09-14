from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.http import HttpResponse
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
            return redirect("menuUsuario")
        
    context = {}
    return render(request, 'criar-login.html', context)

def logoutUsuario(request):
    logout(request)
    return redirect("home")

def registrarUsuario(request):
    form = UserCreationForm()
    if request.method == 'POST':
        resp = UserCreationForm(request.POST)
        if resp.is_valid():
            user = resp.save()
            user.save()

            # Crie uma instância UserProfile associada ao novo usuário com campos vazios
            profile = UserProfile(user=user, academia='', nome='', genero='')
            profile.save()

            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Erro ao responder')
    return render(request, 'criar-login.html', {'form' : form})

def home(request):
    return render(request, 'home.html')


def menuUsuario(request):
    return render(request, 'Menu.html')

def treinos(request):
    return render(request, 'treinos.html')

def perfil(request):
    if request.user.is_authenticated:
        # Recupere o perfil do usuário atualmente logado
        profile = UserProfile.objects.get(user=request.user)


        return render(request, 'perfil.html', {'profile': profile})
    else:
        # Trate o caso em que o usuário não está autenticado    
        # Redirecione para a página de login ou faça algo apropriado
        # Aqui você pode adicionar seu próprio tratamento de erro
        return HttpResponse("Você precisa estar logado para acessar esta página.")
    

def atualizar_perfil(request):
    if request.method == 'POST':
        # Recupere o perfil do usuário atualmente logado
        profile = UserProfile.objects.get(user=request.user)
        
        # Atualize os campos do perfil com base nos dados do formulário
        profile.academia = request.POST['academia']
        profile.nome = request.POST['nome']
        profile.genero = request.POST['genero']
        profile.data_de_nascimento = request.POST['data_de_nascimento']
        
        # Salve as alterações no perfil
        profile.save()
        
        # Redirecione de volta para a página de perfil após a atualização
        return redirect('perfil')
    else:
        # Trate a visualização de atualização de perfil para métodos GET, se necessário
        # Aqui você pode adicionar lógica para exibir um formulário de atualização vazio
        # ou fazer algo apropriado com base em sua necessidade
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'atualizar_perfil.html')  # Crie um template para a página de atualização de perfil se necessário
