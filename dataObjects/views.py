from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, UpdateView

from dataObjects.forms import Create_Obj
from dataObjects.models import Data_Objects, Status_Obj

from utils import get_youtube_live_url


class Home(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        """Get the context for this view."""
        context = {
            # 'link': get_youtube_live_url("@RITTVOficial")
        }

        context.update(kwargs)

        # context['object_list'].filter(id=x[0]).first().quantity = int(update_size.quantity) - int(x[-1])

        return super().get_context_data(**context)


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
class Out_Obj_Create(View):
    http_method_names = ["post", ]

    def post(self, request, *args, **kwargs):
        # obj = Status_Obj.objects.all()
        # print(self.request.POST.get('where-use'))
        list_id = request.POST.getlist('id')
        list_qty = request.POST.getlist('quantity')
        # print((request.POST.getlist('id')))
        for x in range(len(list_id)):
            o = Data_Objects.objects.filter(id=list_id[x]).first()

            obj = Status_Obj.objects.create(
                title=self.request.POST.get('name'),
                date_out=datetime.now(),
                qty_used=list_qty[x],
                local=self.request.POST.get('where-use'),
                last_user=self.request.user,
                obj=o)
            # o.status = obj
            o.quantity = int(o.quantity) - int(list_qty[x])
            o.save()
            obj.save()
        messages.success(request, "Solicitação cadastrada")
        return redirect(reverse('dataObjects:out-obj') + '?success=True')


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
class Out_Obj(ListView):
    template_name = "pages/out-obj.html"
    model = Data_Objects
    context_object_name = "object_list"
    ordering = ['-id']  # ORDERBY

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
            del self.request.session['cart']
            # del self.request.GET['clean']
            return redirect(reverse('dataObjects:out-obj'))

        self.request.session.get('cart')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        passed = True

        try:
            if self.request.session['cart'] is None or type(self.request.session['cart']) != list:
                print("Cria o carrinho", self.request.session['cart'] is None,
                      type(self.request.session['cart']) != list)
                self.request.session['cart'] = []
            # print(len(self.request.session['cart']))
        except KeyError:
            self.request.session['cart'] = []
        nova_lista = []
        for x in self.request.session['cart']:
            if self.request.POST['id'] in x:
                passed = False
                x[-1] = int(x[-1]) + int(self.request.POST['quantity'])
                nova_lista = nova_lista + [x]
            else:
                nova_lista = nova_lista + [x]

        self.request.session['cart'] = nova_lista

        if passed is True:
            if len(self.request.session['cart']) == 0:
                if self.request.POST['quantity'] == "":
                    qty = "1"
                else:
                    qty = self.request.POST['quantity']

                self.request.session['cart'] = [[self.request.POST['id'], self.request.POST['full_name'],
                                                 qty]]
                print("ADD")
            else:
                if self.request.POST['quantity'] == "":
                    qty = "1"
                else:
                    qty = self.request.POST['quantity']

                self.request.session['cart'] = self.request.session['cart'] + (
                    [[self.request.POST['id'], self.request.POST['full_name'],
                      qty]])
                # del self.request.session['cart']
                print("APPEND")
        return redirect(reverse('dataObjects:out-obj'))

    def create(self):
        print(self.request.CREATE)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)

        session = self.request.session.get('cart')
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size
            )
            context = {
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "object_list": queryset,
                "sess": session,
            }
        else:
            context = {
                "paginator": None,
                "page_obj": None,
                "is_paginated": False,
                "object_list": queryset,
                "sess": session,
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)

        # context['object_list'].filter(id=x[0]).first().quantity = int(update_size.quantity) - int(x[-1])

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
        else:
            messages.error(self.request, "Falha no cadastro, preencha corretamente")
        return super().form_valid(form)


class Extern_Request(ListView):
    template_name = "pages/extern-request.html"
    model = Status_Obj
    ordering = ['-id',]

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.filter(type_obj="UNIC")

        return qs


class Return_Obj_Requested(View):
    def post(self, request, *args, **kwargs):
        state = request.POST.get('state')
        id_obj = request.POST.get('id-obj')
        id_status = request.POST.get('id-status')
        obj = Data_Objects.objects.filter(id=id_obj).first()
        status = Status_Obj.objects.filter(id=id_status).first()
        obj.status = state
        obj.quantity = 1
        obj.save()
        status.date_arrived = datetime.now()
        status.save()

        return redirect(reverse('dataObjects:extern-request'))


class Scale_Funcs(TemplateView):
    template_name = "pages/scale-funcs.html"


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
