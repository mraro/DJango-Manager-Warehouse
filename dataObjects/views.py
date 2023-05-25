import os

import dotenv
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, ListView, CreateView

from dataObjects.forms import Create_Obj
from dataObjects.models import Data_Objects, Status_Obj, Requests_To_Out

from utils import get_youtube_live_url, log
from utils.make_pdf import PDF
from utils.paginator import make_pagination
dotenv.load_dotenv()

qtd_page = int(os.environ.get("OBJ_PER_PAGE"))
qty_options = int(os.environ.get("RANGE_PER_PAGE"))
var_url = get_youtube_live_url(os.environ.get("CHANNEL_NAME_YOUTUBE"))


class Home(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):

        """Get the context for this view."""
        context = {
            'url': var_url
            # 'link': get_youtube_live_url("@RITTVOficial")
        }

        context.update(kwargs)

        # context['object_list'].filter(id=x[0]).first().quantity = int(update_size.quantity) - int(x[-1])

        return super().get_context_data(**context)


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
class Out_Obj_Create(CreateView):

    def post(self, request, *args, **kwargs):
        # obj = Status_Obj.objects.all()
        # print(self.request.POST.get('where-use'))
        list_id = request.POST.getlist('id')
        list_qty = request.POST.getlist('quantity')
        user_has_requested = self.request.POST.get('name').title()
        local = self.request.POST.get('where-use').title()
        date_now = datetime.now()
        id_os = Requests_To_Out.objects.create(title=user_has_requested, local=local)
        name_pdf = f"media/docs_out/{id_os}_Saida_{date_now.strftime('%Y-%m-%d_%H-%M')}.pdf"
        id_os.doc_out = name_pdf
        id_os.save()
        data_pdf = []
        user = self.request.user
        description = f"Equipamentos para uso em {local}, sendo o {user_has_requested} responsavel dos itens " \
                      f"descritos abaixo"

        for x in range(len(list_id)):
            equip = Data_Objects.objects.filter(id=list_id[x]).first()

            obj = Status_Obj.objects.create(
                id_os=id_os,
                date_out=date_now,
                qty_used=list_qty[x],
                last_user=user,
                obj=equip)
            # equip.status = obj
            equip.quantity = int(equip.quantity) - int(list_qty[x])
            equip.save()
            obj.save()

            if data_pdf is None:
                data_pdf = [equip.id, equip.name, int(list_qty[x])]
            else:
                data_pdf.append([equip.id, equip.name, int(list_qty[x])])
        log(f'OS ({id_os}) criada pelo: {user}')

        len_table = [20, 150, 20]
        title_table = ['INV', 'Nome do Equipamento', 'Qtd']
        pdf = PDF(user_has_requested, len_table, title_table)
        pdf.alias_nb_pages()

        # hidden details
        pdf.set_title(name_pdf)
        pdf.set_author("https://github.com/mraro")
        pdf.set_creator("https://github.com/mraro")
        pdf.set_subject("Relatório de saida de equipamentos")

        pdf.add_page()
        pdf.print_chapter(data_pdf, description)

        pdf.output("arquivo.pdf", "F")
        log(f'PDF: ({name_pdf}) gerado com o {user}')
        # Save:
        pdf.output(name=name_pdf)

        messages.success(request, "Solicitação cadastrada")
        return redirect(reverse('dataObjects:out-obj') + '?success=True')
        # return redirect(reverse('dataObjects:out-obj'))  # To debug this page


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
class Out_Obj(ListView):
    template_name = "pages/out-obj.html"
    model = Data_Objects
    context_object_name = "object_list"
    ordering = ['-id']  # ORDERBY
    extra_context = {'request_users': Requests_To_Out.objects.all().values_list('title', flat=True).distinct(),
                     'where_to_use': Requests_To_Out.objects.all().values_list('local', flat=True).distinct(),
                     }

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.session.get('cart') is not None:
            for unity in qs:
                for cart_obj in self.request.session.get('cart'):
                    if str(unity.id) == str(cart_obj[0]):
                        unity.quantity = int(unity.quantity) - int(cart_obj[2])
                        # print(f"-{unity.quantity}- -{str(unity.id) == str(cart_obj[0])}-")
        return qs

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('clean') or self.request.GET.get('success'):
            try:
                del self.request.session['cart']
                log("Carrinho esvaziado")
            except KeyError:
                pass

            return redirect(reverse('dataObjects:out-obj'))

        # self.request.session.get('cart')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        passed = True  # avoid mistakes, will return False if exists id on cart session
        # CART
        try:
            # create the cart if it doesn't exist
            if self.request.session['cart'] is None or type(self.request.session['cart']) != list:
                self.request.session['cart'] = []
                log(f'Carrinho criado pelo {user}')
        except KeyError:
            self.request.session['cart'] = []
            log(f'Carrinho criado pelo {user}')

        nova_lista = []
        for x in self.request.session['cart']:
            if self.request.POST['id'] in x:
                passed = False
                x[-1] = int(x[-1]) + int(self.request.POST['quantity'])
                nova_lista = nova_lista + [x]
                print("Reduzindo valores disponiveis na view")
            else:
                nova_lista = nova_lista + [x]
                print("HUM")

        self.request.session['cart'] = nova_lista

        if passed is True:
            if len(self.request.session['cart']) == 0:  # If cart is new create the first else append more
                if self.request.POST['quantity'] == "":
                    qty = "1"
                else:
                    qty = self.request.POST['quantity']

                add_to_cart = [[self.request.POST['id'], self.request.POST['full_name'], qty]]
                self.request.session['cart'] = add_to_cart
                log(f'itens({add_to_cart}) adicionado pelo: {user}')
            else:
                if self.request.POST['quantity'] == "":
                    qty = "1"
                else:
                    qty = self.request.POST['quantity']
                append_to_cart = ([[self.request.POST['id'], self.request.POST['full_name'], qty]])
                self.request.session['cart'] = self.request.session['cart'] + append_to_cart
                log(f'itens({append_to_cart}) adicionado pelo: {user}')
        return redirect(reverse('dataObjects:out-obj'))

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        # page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)

        session = self.request.session.get('cart')

        context = {
            "object_list": queryset,
            "sess": session,
        }

        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)

        return super().get_context_data(**context)


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
class Register(FormView):
    form_class = Create_Obj
    template_name = "pages/register-obj.html"
    success_url = reverse_lazy('dataObjects:home')
    extra_context = {
        "button": "Registrar",
    }

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.success(self.request, "Cadastrado")
            log(f'Obj Criado: {form.cleaned_data} pelo: {self.request.user} ')
        else:
            messages.error(self.request, "Falha no cadastro, preencha corretamente")
        return super().form_valid(form)


class Extern_Request(TemplateView):
    template_name = "pages/extern-request.html"

    def get(self, request, *args, **kwargs):
        research = request.GET.get('q')
        qs = Requests_To_Out.objects.get_big_data(research)
        paginated = make_pagination(request, qs, qtd_page, qty_options)
        qs = paginated['objects_page']
        current_page = paginated['current_page']
        pagination = paginated['pagination']
        kwargs = {
            'list_with_dicts': qs,
            'q': research,
            'current_page': current_page,
            'pagination': pagination,
            'pages': paginated,
        }

            # print((qs[0])['values'])
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        id_req = request.POST.get('id_req')
        description = request.POST.get('description')
        objts = Status_Obj.objects.filter(id_os=id_req)
        for obj in objts:
            obj.last_user = self.request.user
            obj.date_arrived = datetime.now()
            obj.id_os.description = description
            if obj.obj.status == "OK":
                obj.obj.quantity = 1
                obj.obj.save()

            obj.save()
            obj.id_os.save()
        log(f'OS {id_req} fechada pelo: {self.request.user} e ele disse: {description}')

        messages.success(self.request, "Requisição fechada com sucesso")
        return redirect(reverse('dataObjects:extern-request'))


class Communicate(TemplateView):
    template_name = "pages/communicate.html"


"""
- LoginView - exibe um formulário de login e processa os dados de entrada
- LogoutView - encerra a sessão do usuário e redireciona para outra URL
- PasswordChangeView - exibe um formulário para alterar a senha do usuário e processa os dados de entrada
- PasswordResetView - exibe um formulário para redefinir a senha do usuário e processa os dados de entrada
- PasswordResetConfirmView - exibe um formulário para confirmar a redefinição da senha do usuário e processa os dados de entrada

- TemplateView - exibe um único template
- ListView - exibe um conjunto de objetos em um template
- DetailView - exibe detalhes de um objeto específico em um template
- FormView - exibe um formulário e processa dados de entrada
- CreateView - exibe um formulário para criar um novo objeto e processa os dados de entrada
- UpdateView - exibe um formulário para atualizar um objeto existente e processa os dados de entrada
- DeleteView - exibe um formulário para excluir um objeto existente e processa os dados de entrada

- RedirectView - redireciona o usuário para outra URL
- ArchiveIndexView - exibe um índice de objetos arquivados
- YearArchiveView - exibe um índice de objetos arquivados por ano
- MonthArchiveView - exibe um índice de objetos arquivados por mês
- DayArchiveView - exibe um índice de objetos arquivados por dia
- DateDetailView - exibe detalhes de um objeto arquivado específico
- WeekArchiveView - exibe um índice de objetos arquivados por semana
- TodayArchiveView - exibe um índice de objetos arquivados para o dia atual
"""  # noqa
