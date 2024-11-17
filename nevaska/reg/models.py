from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os


def user_directory_path(instance, filename):
    # O caminho será: media/profile_images/<id_do_usuario>/<nome_da_imagem>
    return os.path.join('imagem_perfil', str(instance.id), filename)


class User(AbstractUser):
    rca = models.CharField(max_length=3, null=True, blank=True)
    cargos = models.CharField(choices=[('VENDEDOR', 'Vendedor'), (
        'GERENTE', 'Gerente'), ('SUPERVISOR', 'Supervisor')], max_length=25, null=True)

    first_name = models.CharField(max_length=100, null=True)
    img = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):

        return self.username


def local_arq(instance, filename):
    # Aqui estamos criando o caminho completo com a pasta que você deseja
    directory = os.path.join(
        settings.MEDIA_ROOT, f'anexos/Empresas/{instance.owner.id}/')

    # Cria o diretório se ele não existir
    os.makedirs(directory, exist_ok=True)

    # Retorna o caminho relativo dentro de MEDIA_ROOT para salvar o arquivo
    return os.path.join(f'anexos/Empresas/{instance.owner.id}/', filename)


class Empresa(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_form = models.DateField(default='2024-01-01')
    situacao_cliente = models.CharField(max_length=50, default='Cadastro')
    cod_cliente = models.CharField(max_length=10, default='0000')
    emp_cnpj = models.CharField(max_length=18, default='00.000.000/0000-00')
    emp_cpf = models.CharField(max_length=14, default='000.000.000-00')
    emp_ie = models.CharField(max_length=9, default='000.000')
    tipo_cliente = models.CharField(max_length=50, default='')
    razao_nome = models.CharField(max_length=255, default='')
    fantasia_nome = models.CharField(max_length=255, default='')
    cep = models.CharField(max_length=9, default='00000-000')
    rua = models.CharField(max_length=255, default='Rua exemplo')
    bairro = models.CharField(max_length=255, default='Bairro exemplo')
    cidade = models.CharField(max_length=255, default='Cidade exemplo')
    estado = models.CharField(max_length=2, default='XX')
    complemento = models.CharField(max_length=255, null=True, default="")
    produto_desc = models.CharField(max_length=255, default='Produto padrão')
    valor_desc = models.CharField(max_length=255, null=True)
    prazo_desc = models.CharField(max_length=255, null=True)
    comp_emp = models.CharField(max_length=255, null=True)
    num_endr = models.CharField(max_length=10, null=True)
    email_empresa = models.CharField(max_length=255, null=True)
    telefone_empresa = models.CharField(max_length=255, null=True)

    # Referências comerciais
    referencia1 = models.CharField(max_length=255, default='Referência 1')
    contato1 = models.CharField(max_length=20, default='(00) 0000-0000')
    referencia2 = models.CharField(max_length=255, default='Referência 2')
    contato2 = models.CharField(max_length=20, default='(00) 0000-0000')
    referencia3 = models.CharField(max_length=255, default='Referência 3')
    contato3 = models.CharField(max_length=20, default='(00) 0000-0000')
    referencia4 = models.CharField(max_length=255, default='Referência 4')
    contato4 = models.CharField(max_length=20, default='(00) 0000-0000')
    referencia5 = models.CharField(max_length=255, default='Referência 5')
    contato5 = models.CharField(max_length=20, default='(00) 0000-0000')

    # Resultado Ficha

    result = models.CharField(choices=[('APROVADO', 'Aprovado'), ('REPROVADO', 'Reprovado'), (
        'EM ANALISE', 'Em Analise'), ('EM ABERTO', 'Em Aberto')], max_length=100, null=True, blank=True)

    def __str__(self):
        return self.razao_nome


class Arquivos_empresa(models.Model):
    # migrate
    name = models.CharField(max_length=255, null=True)
    arquivo = models.FileField(upload_to=local_arq,  null=True)
    owner = models.ForeignKey(
        Empresa, related_name="arquivos_empresas", on_delete=models.SET_NULL, null=True)
