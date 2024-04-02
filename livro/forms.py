from django import forms
from .models import Livro
from django.db import models
from datetime import date
from .models import Categoria

###colocar em fields após ediçao de dados que serao selecionados

class CadastroLivro(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()

class CategoriaLivro(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'       


