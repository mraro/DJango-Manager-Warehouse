from django.contrib import messages

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, ListView

from dataObjects.forms import Create_Obj
from dataObjects.models import Data_Objects


# Create your views here.

class Home(TemplateView):
    template_name = "pages/home.html"


class Out_Obj(ListView):
    template_name = "pages/out-obj.html"
    model = Data_Objects
    context_object_name = "object_list"
    ordering = ['-id']  # ORDERBY

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('clean'):
            del self.request.session['cart']
            # del self.request.GET['clean']
            return redirect(reverse('dataObjects:out-obj'))

        # print(self.request.GET['clean'])
        # breakpoint()
        self.request.session.get('cart')
        # except KeyError:
        #     self.request.session['cart'] = []
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        passed = True

        try:
            if self.request.session['cart'] is None or type(self.request.session['cart']) != list:
                print("Cria o carrinho", self.request.session['cart'] is None,
                      type(self.request.session['cart']) != list)
                self.request.session['cart'] = []
            print(len(self.request.session['cart']))
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


class Register(FormView):
    form_class = Create_Obj
    template_name = "pages/register-obj.html"
    success_url = reverse_lazy('dataObjects:home')

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.success(self.request, "Cadastrado")
        else:
            messages.error(self.request, "Falha no cadastro, preencha corretamente")
        return super().form_valid(form)


class Extern_Request(TemplateView):
    template_name = "pages/extern-request.html"


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
