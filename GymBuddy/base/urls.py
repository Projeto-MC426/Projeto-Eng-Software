from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.paginaLogin, name='paginaLogin'),
    path('logout/', views.logoutUsuario, name='paginaLogout'),
    path('registrar/', views.registrarUsuario, name='registrar'),
    path('menuUsuario/', views.menuUsuario, name = 'menuUsuario'),
    path('treinos/', views.treinos, name='treinos'),
    path('perfil/', views.perfil, name='perfil'),
    path('atualizar_perfil/', views.atualizar_perfil, name='atualizar_perfil')
]