from django.shortcuts import render,redirect
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livro , Categoria , Emprestimo
from .forms import CadastroLivro,CategoriaLivro
from datetime import datetime
from django.db.models import Q


def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario'])
        status_categoria = request.GET.get('cadastro_categoria')
        livros = Livro.objects.filter(usuario = usuario)
        total_livros = livros.count()
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form_categoria = CategoriaLivro()
        usuarios = Usuario.objects.all()

        livros_emprestar = Livro.objects.filter(usuario = usuario).filter(emprestado = False)
        livros_emprestados = Livro.objects.filter(usuario = usuario).filter(emprestado = True)

        return render(request, 'home.html',{'livros':livros,
                                             'usuario_logado': request.session.get('usuario'),
                                             'form':form, 'status_categoria': status_categoria,
                                             'form_categoria':form_categoria,
                                             'usuarios': usuarios,
                                             'livros_emprestar': livros_emprestar,
                                             'total_livros': total_livros,
                                             'livros_emprestados':livros_emprestados})
    else:
        return redirect('/auth/login/?status=2')
    

### verifica se o usuario esta logado e se sim mostra os livros que são dele    
def ver_livros(request, id):
    if request.session.get('usuario'):
        livro = Livro.objects.get(id = id)
        if request.session.get('usuario') == livro.usuario.id:
            usuario = Usuario.objects.get(id = request.session['usuario'])
            categoria_livro = Categoria.objects.all
            emprestimos = Emprestimo.objects.filter(livro = livro)
            form = CadastroLivro()
            form.fields['usuario'].initial = request.session['usuario']

            form_categoria = CategoriaLivro()
            usuarios = Usuario.objects.all()
            livros_emprestar = Livro.objects.filter(usuario = usuario).filter(emprestado = False)
            livros_emprestados = Livro.objects.filter(usuario = usuario).filter(emprestado = True)
            return render(request,'ver_livro.html', {'livro': livro, 'categoria_livro': categoria_livro,
                                                     'emprestimos':emprestimos,
                                                     'usuario_logado': request.session.get('usuario'),
                                                     'form':form,'id_livro':id,
                                                     'form_categoria':form_categoria,
                                                     'usuarios': usuarios,
                                                     'livros_emprestar': livros_emprestar,
                                                     'livros_emprestados':livros_emprestados})
        else:
            return HttpResponse('Esse livro não é seu')
        
def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('/livro/home')
        else:
            HttpResponse('Dados invalidos')

def excluir_livro(request, id):
    livro = Livro.objects.get(id = id).delete()
    return redirect('/livro/home')

def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)

    if form.is_valid():
        form.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        HttpResponse('Dados não validos')

def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        livro_emprestado = request.POST.get('livro_emprestado')

        emprestimo = Emprestimo(nome_emprestado_id = nome_emprestado, livro_id = livro_emprestado)
        emprestimo.save()

        livro = Livro.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()

        return redirect('/livro/home')
    
def devolver_livro(request):
    id = request.POST.get('id_livro_devolver')
    livro_devolver = Livro.objects.get(id = id)
    livro_devolver.emprestado = False
    livro_devolver.save()

    emprestimo_devolver = Emprestimo.objects.get(Q(livro = livro_devolver)& Q(data_devolucao = None))
    emprestimo_devolver.data_devolucao = datetime.now()
    emprestimo_devolver.save()

    return redirect('/livro/home')

def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    categoria_id = request.POST.get('categoria_id')
    categoria = Categoria.objects.get(id = categoria_id)
    
    livro = Livro.objects.get(id = livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.categoria = categoria
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    else:
        return redirect('/auth/sair')
    
def livros_devolver(request):
    usuario = Usuario.objects.get(id = request.session['usuario'])
    emprestimos = Emprestimo.objects.filter(nome_emprestado = usuario)
    print(emprestimos)

    return render(request, 'livros_devolver.html', {'usuario_logado': request.session['usuario'],
                                                    'emprestimos': emprestimos})

def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    id_livro = request.POST.get('id_livro')
    

    emprestimo = Emprestimo.objects.get(id = id_emprestimo)
    if emprestimo.livro.usuario.id == request.session['usuario']:
        emprestimo.avaliacao = opcoes
        emprestimo.save()
        return redirect(f'/livro/ver_livro/{id_livro}')
    else:
        return HttpResponse('Este empréstimo nao é seu')


    
