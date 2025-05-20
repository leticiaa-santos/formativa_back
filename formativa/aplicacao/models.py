from django.db import models
from django.contrib.auth.models import AbstractUser

# models para a criação do usuário
class Usuario(AbstractUser):
    TIPO_CHOICHES = [
        ('G', 'gestor'),
        ('P', 'professor'),
    ]

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICHES, default='P')
    ni = models.IntegerField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField()
    data_contratacao = models.DateField()

    REQUIRED_FIELDS = ['ni', 'data_nascimento', 'data_contratacao', 'tipo']

    def __str__(self):
        return f'{self.username} ({self.get_tipo_display()})' # função para mostrar o valor da chave no dicionário de escolhas

# models para a criação da disciplina
class Disciplina(models.Model):
    nome = models.CharField(max_length=255)
    curso = models.CharField(max_length=255)
    carga_horaria = models.IntegerField()
    descricao = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'tipo': 'P'}) # chave estrangeira que limita a ser somente um professor a ser responsável pela matéria

    def __str__(self):
        return self.nome
    
# models para a criação das salas
class Sala(models.Model):
    nome = models.CharField(max_length=255)
    capacidade = models.IntegerField()

    def __str__(self):
        return self.nome
    
# models para a criação de reserva de ambientes
class ReservaAmbiente(models.Model):
    PERIODO_CHOICES = [
        ('M', 'manhã'),
        ('T', 'tarde'),
        ('N', 'noite'),
    ]

    data_inicio = models.DateField()
    data_termino = models.DateField()
    periodo = models.CharField(max_length=1, choices=PERIODO_CHOICES, default='M')
    sala_reservada = models.ForeignKey(Sala, on_delete=models.CASCADE)
    professor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo': 'P'})
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sala_reservada} - {self.get_periodo_display()} ({self.data_inicio}) a ({self.data_termino})'



