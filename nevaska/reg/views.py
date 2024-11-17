from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Empresa, Arquivos_empresa, User
from django.contrib import messages
from django.http import Http404
from .forms import ArquivosForm
from django.core.paginator import Paginator



@login_required
def salvar_cadastro(request):
    if request.method == 'POST':
        # Usando get() para garantir valores padrão caso o campo não tenha sido preenchido
        data_form = request.POST.get('data_form', '2024-01-01')
        situacao_cliente = request.POST.get('situacao_cliente', 'Cadastro')
        cod_cliente = request.POST.get('cod_cliente', '0000')
        emp_cnpj = request.POST.get('emp_cnpj', '00.000.000/0000-00')
        emp_cpf = request.POST.get('emp_cpf', '000.000.000-00')
        emp_ie = request.POST.get('emp_ie', '000.000')
        tipo_cliente = request.POST.get('tipo_cliente', 'Revenda')
        razao_nome = request.POST.get('razao_nome', 'Razão Social')
        fantasia_nome = request.POST.get('fantasia_nome', 'Nome Fantasia')
        cep = request.POST.get('cep', '00000-000')
        rua = request.POST.get('rua', 'Rua exemplo')
        bairro = request.POST.get('bairro', 'Bairro exemplo')
        cidade = request.POST.get('cidade', 'Cidade exemplo')
        estado = request.POST.get('uf', 'XX')
        ibge = request.POST.get('ibge', '0000000')
        produto_desc = request.POST.get('produto_desc', 'Produto padrão')
        valor_desc = request.POST.get('valor_desc', '0.00')
        prazo_desc = request.POST.get('prazo_desc', '30')

        comp_emp = request.POST.get('comp_emp')
        num_endr = request.POST.get('num_endr')
        email_empresa = request.POST.get('email_empresa')
        telefone_empresa = request.POST.get('telefone_empresa')

        referencia1 = request.POST.get('referencia1', 'Referência 1')
        contato1 = request.POST.get('contato1', '(00) 0000-0000')
        referencia2 = request.POST.get('referencia2', 'Referência 2')
        contato2 = request.POST.get('contato2', '(00) 0000-0000')
        referencia3 = request.POST.get('referencia3', 'Referência 3')
        contato3 = request.POST.get('contato3', '(00) 0000-0000')
        referencia4 = request.POST.get('referencia4', 'Referência 4')
        contato4 = request.POST.get('contato4', '(00) 0000-0000')
        referencia5 = request.POST.get('referencia5', 'Referência 5')
        contato5 = request.POST.get('contato5', '(00) 0000-0000')

        # Criando a instância do modelo e salvando no banco de dados
        empresa = Empresa(
            data_form=data_form,
            situacao_cliente=situacao_cliente,
            cod_cliente=cod_cliente,
            emp_cnpj=emp_cnpj,
            emp_cpf=emp_cpf,
            emp_ie=emp_ie,
            tipo_cliente=tipo_cliente,
            razao_nome=razao_nome,
            fantasia_nome=fantasia_nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            produto_desc=produto_desc,
            valor_desc=valor_desc,
            prazo_desc=prazo_desc,
            referencia1=referencia1,
            contato1=contato1,
            referencia2=referencia2,
            contato2=contato2,
            referencia3=referencia3,
            contato3=contato3,
            referencia4=referencia4,
            contato4=contato4,
            referencia5=referencia5,
            contato5=contato5,
            comp_emp=comp_emp,
            num_endr=num_endr,
            email_empresa=email_empresa,
            telefone_empresa=telefone_empresa,
            owner=request.user
        )

        # Salvando no banco de dados
        empresa.save()
        return redirect('home')

    else:
        return render(request, 'index.html')


@login_required
def home(request):
    profile = User.objects.get(id=request.user.id)
    return render(request, 'home.html', {'titulo': 'Grupo Nevaska', 'profile': profile})


def cadastro(request):
    res = render(request, 'registro.html')
    return res


def cadastros_list(request):
    if request.user.cargos == 'SUPERVISOR':
        empresas_list = Empresa.objects.all()
    elif request.user.cargos == 'VENDEDOR':
        empresas_list = Empresa.objects.filter(vendedor=request.user)
    else:
        empresas_list = Empresa.objects.filter(owner=request.user)

    paginator = Paginator(empresas_list, 10)  # Mostra 10 empresas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'cadastros_list.html', context)


@login_required
def detalhes_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    arquivos = Arquivos_empresa.objects.filter(owner=empresa)

    if request.method == 'POST':

        form = ArquivosForm(request.POST, request.FILES)
        if form.is_valid():

            novo_arquivo = Arquivos_empresa(
                arquivo=request.FILES['arquivo'],
                name=request.POST['name'],
                owner=empresa
            )
            print(request.FILES)
            novo_arquivo.save()

            return redirect('detalhes-emp', id=empresa.id)
    else:
        form = ArquivosForm()

    context = {
        'empresa': empresa,
        'form': form,
        'arquivos': arquivos,
    }
    return render(request, 'detalhes.html', context)


def excluir_arquivo(request, arquivo_id):

    arquivo = get_object_or_404(Arquivos_empresa, id=arquivo_id)
    arquivo.delete()

    return redirect('detalhes-emp', id=arquivo.owner.id)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos!")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def editar_perfil(request):
    try:
        profile = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        raise Http404("Perfil não encontrado")

    if request.method == 'POST':
        # Pega o arquivo enviado no campo 'imagem'
        imagem = request.FILES.get('imagem')
        if imagem:
            # Se o usuário enviou uma imagem, salva a imagem
            profile.img = imagem
        # Atualiza os outros campos, se necessário
        profile.first_name = request.POST.get('nome')
        profile.cargos = request.POST.get('cargo')
        profile.rca = request.POST.get('rca')
        # Salva as alterações
        profile.save()
        return redirect('editar_perfil')  # Redireciona após salvar

    context = {
        'profile': profile,

    }

    return render(request, 'painel.html', context)


def criar_usuario(request):
    if request.method == 'POST':
        # Pega os dados do formulário
        username = request.POST.get('username')
        first_name = request.POST.get('name')
        cargos = request.POST.get('cargo')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verifica se todos os campos obrigatórios foram preenchidos
        if not username or not first_name or not email or not password:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('criar_usuario')

        # Cria o usuário no banco de dados
        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                cargos=cargos,
                email=email,
                password=password
            )

            messages.success(request, "Usuário criado com sucesso!")
            return redirect('home')  # Redireciona para a página inicial
        except Exception as e:
            messages.error(request, f"Erro ao criar o usuário: {str(e)}")
            return redirect('criar_usuario')

    return render(request, 'painel.html')


@login_required
def resultado_analise(request, pk):
    try:
        analise = Empresa.objects.get(id=pk)
    except Empresa.DoesNotExist:

        return redirect('lista_empresas')

    if request.method == 'POST':
        result = request.POST.get('result')

        analise.result = result
        analise.save()

        return redirect('home')

    else:
        return render(request, 'cadastros_list.html', {'analise': analise})
