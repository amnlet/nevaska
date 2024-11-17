from django.urls import path

from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='registro'),
    path('lista/', views.cadastros_list, name='lista'),
    path('salvar-cadastro/', views.salvar_cadastro, name='salvar_cadastro'),

    path('detalhes_empresa/id=<str:id>',
         views.detalhes_empresa, name='detalhes-emp'),
    path('excluir_arquivo/<int:arquivo_id>/',
         views.excluir_arquivo, name='excluir_arquivo'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # Página inicial após o login

    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('criar-usuario/', views.criar_usuario, name='criar_usuario'),
    path('resultado_analise/<int:pk>', views.resultado_analise, name='resultado'),
]
