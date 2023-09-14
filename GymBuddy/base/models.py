from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    academia = models.CharField(max_length=100, unique=True)
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=10)
    data_de_nascimento = models.DateField(null=True, blank=True)
    # Outros campos do perfil aqui

    def __str__(self):
        return self.user.username