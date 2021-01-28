from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
from .models import ArrobaModel
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    return render(request, 'index.html')


def cadastro(request):
    if request.method == "GET":
        cadastro_form = forms.CadastroForms()
        contexto = {
            'cadastro_form': cadastro_form
    }

        return render(request, 'cadastro.html', contexto)

    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']

        if senha != senha2:
            return redirect('cadastro')
        
        if User.objects.filter(email=email).exists():
            return redirect('cadastro')

        user = User.objects.create_user(
            username=nome,
            email=email,
            password=senha
        )

        user.save()

        return redirect('login')


def login(request):
    if request.method == "GET":
        login_form = forms.LoginForms()
        contexto = {
            'login_form': login_form
    }

        return render(request, 'login.html', contexto)
    
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if User.objects.filter(email=email).exists():
            nome = (User.objects.filter(email=email).
                values_list('username', flat=True).get())
            user = auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request, user)

            return redirect('index')

        else:
            return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id 
        lista_arrobas = ArrobaModel.objects.filter(user_id=request.user)
        contexto = {
            'id': id,
            'lista_arrobas': lista_arrobas
        }

        return render(request, 'dashboard.html', contexto)


def cadastro_arroba(request):
    if request.method == "GET":
        arroba_form = forms.ArrobaForms()
        contexto = {
            'arroba_form': arroba_form
        }

        return render(request, 'cadastro_arroba.html', contexto)

    if request.method == "POST":
        arroba = request.POST['arroba']
        user = get_object_or_404(User, pk=request.user.id)

        if ArrobaModel.objects.filter(arroba=arroba).exists():
            return redirect('dashboard')

        twitter_arroba = ArrobaModel(arroba=arroba, user_id=user)
        twitter_arroba.save()

        return redirect('dashboard')

        
def deleta_arroba(request, arroba_id):
    if request.user.is_authenticated:
        arroba = get_object_or_404(ArrobaModel, pk=arroba_id)
        arroba.delete()
        return redirect('dashboard')

    