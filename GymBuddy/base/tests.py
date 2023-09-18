from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile

class PerfilTestCase(TestCase):
    def setUp(self):
        
        # Criar um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.save()

        # Crie um perfil para o usuário
        self.profile = UserProfile.objects.create(user=self.user, academia='Gym', nome='Test User', genero='M')

    def test_atualizar_perfil_com_credenciais_corretas(self):
        # Faça login como o usuário de teste
        self.client.login(username='testuser', password='testpass')

        # Simule uma postagem para atualizar o perfil com dados válidos
        response = self.client.post(reverse('atualizar_perfil'), {
            'academia': 'New Gym',
            'nome': 'Updated User',
            'genero': 'F',
            'data_de_nascimento': '2000-01-01',  # Uma data válida
        })

        # Verifique se a resposta redireciona para a página 'perfil'
        self.assertRedirects(response, reverse('perfil'))

        # Recarregue o perfil do banco de dados para verificar as atualizações
        updated_profile = UserProfile.objects.get(user=self.user)

        # Verifique se os campos foram atualizados corretamente
        self.assertEqual(updated_profile.academia, 'New Gym')
        self.assertEqual(updated_profile.nome, 'Updated User')
        self.assertEqual(updated_profile.genero, 'F')
        self.assertEqual(str(updated_profile.data_de_nascimento), '2000-01-01')

    def test_atualizar_perfil_sem_data_de_nascimento(self):
        # Faça login como o usuário de teste
        self.client.login(username='testuser', password='testpass')

        # Simule uma postagem para atualizar o perfil sem fornecer data de nascimento
        response = self.client.post(reverse('atualizar_perfil'), {
            'academia': 'New Gym',
            'nome': 'Updated User',
            'genero': 'F',
        })

        # Verifique se a resposta renderizou a página 'atualizar_perfil.html' novamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atualizar_perfil.html')

        # Verifique se uma mensagem de erro foi exibida no campo 'data_de_nascimento'
        self.assertContains(response, 'Data de Nascimento é um campo obrigatório')


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

