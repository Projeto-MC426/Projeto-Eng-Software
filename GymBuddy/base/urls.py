from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.paginaLogin, name='paginaLogin'),
    path('logout/', views.logoutUsuario, name='paginaLogout'),

]