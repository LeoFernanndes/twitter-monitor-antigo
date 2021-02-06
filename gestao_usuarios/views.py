from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
from .models import ArrobaModel
from django.shortcuts import get_object_or_404
from . import twitter_api
from . import twitter_database
import pandas as pd
import json
import unicodedata
from django.utils import encoding
from django.core.paginator import Paginator

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
        
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        else:
        
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

            return redirect('dashboard')

        else:
            return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        
        id = request.user.id 
        
        lista_arrobas = ArrobaModel.objects.filter(user_id=request.user)
        paginator = Paginator(lista_arrobas, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        contexto = {
            'id': id,
            'lista_arrobas': page_obj
        }

        return render(request, 'dashboard.html', contexto)
    
    else:
        return redirect('index')
        

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

        """
        if ArrobaModel.objects.filter(arroba=arroba).exists():
            return redirect('dashboard')
        """

        if twitter_api.validate_user(arroba):
            arroba_attributes = twitter_api.get_arroba_attributes(arroba)
            
            normal_image_url = arroba_attributes.profile_image_url
            larger_image_url = normal_image_url.split('_normal')[0] + normal_image_url.split('_normal')[1]
            
            twitter_arroba = ArrobaModel(arroba=arroba, profile_image_url=larger_image_url, user_id=user,
            description=arroba_attributes.description,
            name=arroba_attributes.name)
            
            twitter_arroba.save()

            return redirect('dashboard')

        else:
            return redirect('cadastro_arroba')

        
def deleta_arroba(request, arroba_id):
    if request.user.is_authenticated:
        arroba = get_object_or_404(ArrobaModel, pk=arroba_id)
        arroba.delete()
        return redirect('dashboard')

"""
def detalha_arroba(request, arroba_id):
    if request.user.is_authenticated:
        arroba = get_object_or_404(ArrobaModel, pk=arroba_id)
        

        mydb = twitter_database.mysql_rds_database_authentication('twitter_data')
        df_tweets = pd.read_sql(f"SELECT * FROM tweets where arroba = '{arroba.arroba}';", con=mydb).sort_values(by='date', ascending=False)
        df_tweets['date'] = df_tweets['date'].astype(str)
        string_tweets = df_tweets.head(10).to_json(orient='records')
        json_tweets = json.loads(string_tweets)
         

        contexto = {
            'arroba':arroba,
            'len': df_tweets.shape,
            'json_tweets': json_tweets
        }

        return render(request, 'detalhes_arroba.html', context=contexto)
"""        
        
def detalha_arroba(request, arroba_id):
    if request.user.is_authenticated:
        arroba = get_object_or_404(ArrobaModel, pk=arroba_id)
        

        mydb = twitter_database.mysql_rds_database_authentication('twitter_data')
        df_tweets = pd.read_sql(f"SELECT * FROM tweets where arroba = '{arroba.arroba}';", con=mydb).sort_values(by='date', ascending=False)
        df_tweets['date'] = df_tweets['date'].astype(str)
        string_tweets = df_tweets.to_json(orient='records')
        json_tweets = json.loads(string_tweets)

        paginator = Paginator(json_tweets, 10)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1
            
        page_obj = paginator.get_page(page_number)
        limite_inf_pag = int(page_number) - 5
        limite_sup_pag = int(page_number) + 5
        last_page = int(paginator.num_pages)

        contexto = {
            'arroba':arroba,
            'len': df_tweets.shape,
            'json_tweets': json_tweets,
            'paginated_json_tweets': page_obj,
            'limite_inf_pag': limite_inf_pag,
            'limite_sup_pag': limite_sup_pag,
            'last_page': last_page
            
        }

        return render(request, 'detalhes_arroba.html', context=contexto)