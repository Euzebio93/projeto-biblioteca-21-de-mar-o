from django.contrib import admin
from .models import Livro,Categoria,Emprestimo

admin.site.register(Livro)
admin.site.register(Categoria)
admin.site.register(Emprestimo)

