from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTestCase(TestCase):
    def test_pagina_login_existe(self):
        response = self.client.get(reverse('paginaLogin'))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.username = 'usuarioteste'
        self.password = 'senhateste'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_com_credenciais_validas(self):
        response = self.client.post(reverse('paginaLogin'), {'usuario': self.username, 'senha': self.password})
        self.assertEqual(response.status_code, 302)  # Verifica se é redirecionado após o login
        self.assertRedirects(response, reverse('menuUsuario'))
    
    def test_login_com_credenciais_invalidas(self):
        response = self.client.post(reverse('paginaLogin'), {'usuario': 'usuario_invalido', 'senha': 'senha_errada'})
        self.assertEqual(response.status_code, 200)  # Permanece na página de login
        self.assertContains(response, 'Usuario não encontrado')  # Verifique se a mensagem de erro é exibida

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('paginaLogout'))
        self.assertEqual(response.status_code, 302)  # Verifica se é redirecionado após o logout
        self.assertRedirects(response, reverse('home'))

    def test_registro_usuario_valido(self):
        response = self.client.post(reverse('registrar'), {'username': 'novousuario', 'password1': 'senhavalida', 'password2': 'senhavalida'})
        self.assertEqual(response.status_code, 302)  # Verifica se é redirecionado após o registro
        self.assertRedirects(response, reverse('home'))
    
    def test_registro_usuario_invalido(self):
        response = self.client.post(reverse('registrar'), {'username': 'novousuario', 'password1': 'senhavalida', 'password2': 'senhadiferente'})
        self.assertEqual(response.status_code, 200)  # Permanece na página de registro
        self.assertContains(response, 'Erro ao responder')  # Verifica se a mensagem de erro é exibida

