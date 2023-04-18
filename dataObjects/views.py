from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class Home(TemplateView):
    template_name = "pages/home.html"


class Out_Obj(TemplateView):
    template_name = "pages/home.html"


class Register(TemplateView):
    template_name = "pages/home.html"


class Extern_Request(TemplateView):
    template_name = "pages/home.html"


class Scale_Funcs(TemplateView):
    template_name = "pages/home.html"


class Communicate(TemplateView):
    template_name = "pages/home.html"
