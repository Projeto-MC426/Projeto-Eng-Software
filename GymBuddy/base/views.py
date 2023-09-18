from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.http import HttpResponse
from django.forms import ValidationError
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
    # Recupere o perfil do usuário atualmente logado
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Se a solicitação for POST, atualize o perfil
        profile.academia = request.POST['academia']
        profile.nome = request.POST['nome']
        profile.genero = request.POST['genero']
        
        # Tente obter a data de nascimento do formulário
        data_de_nascimento = request.POST.get('data_de_nascimento', None)

        if data_de_nascimento:
            try:
                # Tente converter a data de nascimento
                profile.data_de_nascimento = data_de_nascimento
                profile.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('perfil')
            except ValidationError as e:
                # Trate o caso de validação da data de nascimento
                messages.error(request, f"Erro: {', '.join(e)}")
        else:
            # Trate o caso em que a data de nascimento não foi fornecida
            messages.error(request, "Data de Nascimento é um campo obrigatório.")

    return render(request, 'perfil.html', {'profile': profile})
    
def atualizar_perfil(request):
    # Recupere o perfil do usuário atualmente logado
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Atualize os campos do perfil com base nos dados do formulário
        profile.academia = request.POST['academia']
        profile.nome = request.POST['nome']
        profile.genero = request.POST['genero']
        
        # Tente obter a data de nascimento do formulário
        data_de_nascimento = request.POST.get('data_de_nascimento', None)

        if data_de_nascimento:
            try:
                # Tente converter a data de nascimento
                profile.data_de_nascimento = data_de_nascimento
                profile.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('perfil')
            except ValidationError as e:
                # Trate o caso de validação da data de nascimento
                messages.error(request, f"Erro: {', '.join(e)}")
        else:
            # Trate o caso em que a data de nascimento não foi fornecida
            messages.error(request, "Data de Nascimento é um campo obrigatório.")

    return render(request, 'atualizar_perfil.html', {'profile': profile})