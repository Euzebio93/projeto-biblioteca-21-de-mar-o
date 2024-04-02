from django.db import models
from datetime import date
import datetime
from usuarios.models import Usuario

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()

    def __str__(self) -> str:
        return self.nome
    


class Livro(models.Model):
    img = models.ImageField(upload_to='capa_livro', null=True, blank=True)
    #TODO: colocar imagem como obrigatoria no momento do cadastro.
    nome = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 30)
    data_cadastro = models.DateField(default = date.today)
    emprestado = models.BooleanField(default = False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null = True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null = True)



    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    choices = (
        ('P', 'Pessimo'),
        ('R', 'Ruim'),
        ('M', 'Mediano'),
        ('B', 'Bom'),
        ('O', 'Otimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null = True)
    data_emprestimo = models.DateTimeField(default =datetime.datetime.now())
    data_devolucao = models.DateTimeField(blank = True, null = True)
    livro = models.ForeignKey(Livro, on_delete=models.SET_NULL, null = True)
    avaliacao = models.CharField(max_length = 1, choices=choices, null = True, blank = True)

    def __str__(self) -> str:
        return f"{self.nome_emprestado} | {self.livro}"
    
