from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'status', 'prioridade', 'prazo', 'projeto', 'usuario_atribuido']
        widgets = {
            'prazo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'projeto': forms.Select(),
            'usuario_atribuido': forms.HiddenInput(),  # Oculta o campo no formulário
        }