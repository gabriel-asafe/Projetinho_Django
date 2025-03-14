from django.db import models
from accounts.models import User

class Project(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projetos_criados')
    membros = models.ManyToManyField(User, related_name='projetos_participados')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome