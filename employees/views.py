from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from employees.form import Reg_Emp_Form


class Login_Employees(LoginView):
    template_name = 'pages/login.html'
    next_page = "dataObjects:home"

    extra_context = {
        "button": "Login",
    }


class Logout_Employees(LogoutView):
    next_page = "dataObjects:home"


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
@method_decorator(permission_required(login_url="dataObjects:home", perm="admin",), name='dispatch')
class Register_Employees(FormView):
    form_class = Reg_Emp_Form
    template_name = "pages/login.html"
    extra_context = {
        "button": "Cadastro",
    }

    def get_context_data(self, **kwargs):
        session_data = self.request.session.get('register_form_data')
        # self.form_class = RegisterForm(session_data)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': Reg_Emp_Form(session_data),
        })
        return context

    def post(self, request, *args, **kwargs):
        POST = request.POST  # Receive data by POST
        request.session['register_form_data'] = POST  # Give data from POST to SESSION
        form = Reg_Emp_Form(POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()
                messages.success(request, "User registered successfully!!!")
                del (request.session['register_form_data'])  # kill session
                return redirect('dataObjects:home')
            except ValueError:
                messages.error(request, "Fail in create user")
                return redirect('employees:register')

        return redirect('employees:register')
