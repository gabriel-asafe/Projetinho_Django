from django.db import models
from accounts.models import User
from projects.models import Project

class Task(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
    ]
    PRIORITY_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    prioridade = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='baixa')
    prazo = models.DateTimeField()
    usuario_atribuido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tarefas')
    projeto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tarefas', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    def is_atrasado(self):
        from django.utils import timezone
        return self.status != 'concluido' and self.prazo < timezone.now()