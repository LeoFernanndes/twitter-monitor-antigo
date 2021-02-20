from django import forms
from . import twitter_api
from .models import ArrobaModel
from django.contrib.auth.models import User
from django.contrib import auth

class CadastroForms(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)
    senha2 = forms.CharField(label='Confirmação de senha', max_length=100, widget=forms.PasswordInput)


class LoginForms(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)
    
    def get_request(self, request):
        self.request = request
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Usuário não cadastrado")
        
        return email


    def clean_senha(self):
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")
        
        if User.objects.filter(email=email).exists():
            nome = (User.objects.filter(email=email).
                values_list('username', flat=True).get())
            user = auth.authenticate(self.request, username=nome, password=senha)

            if user is None:
                raise forms.ValidationError("Senha incorreta")
        
        
        return senha
       

class ArrobaForms(forms.Form):
    arroba = forms.CharField(label='Arroba sem @', max_length=100)
    
    def get_request(self, request):
        self.request = request
    
    
    def clean_arroba(self):
        arroba = self.cleaned_data.get("arroba")
        
        if not twitter_api.validate_user(arroba):
            raise forms.ValidationError("O perfil inserido não existe")
         
         
        lista_arrobas = ArrobaModel.objects.filter(user_id=self.request.user)
        lista_arrobas = [arroba.arroba for arroba in lista_arrobas]
        if arroba in lista_arrobas:
            raise forms.ValidationError("O perfil já está cadastrado")
            
            
        if twitter_api.validate_user(arroba):
            return arroba
            