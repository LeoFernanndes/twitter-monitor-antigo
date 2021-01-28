from django import forms

class CadastroForms(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)
    senha2 = forms.CharField(label='Confirmação de senha', max_length=100, widget=forms.PasswordInput)


class LoginForms(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)


class ArrobaForms(forms.Form):
    arroba = forms.CharField(label='Arroba', max_length=100)