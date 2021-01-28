from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('cadastro_arroba', views.cadastro_arroba, name='cadastro_arroba'),
    path('deleta_arroba/<int:arroba_id>', views.deleta_arroba, name='deleta_arroba'),
]