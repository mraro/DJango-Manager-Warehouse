from django.views.generic import FormView, TemplateView

from pgms.forms import Form_PGM


# Create your views here.

class View_Pgms_Available(FormView):
    template_name = "pages/scale-pgms.html"
    form_class = Form_PGM
    extra_context = {
        'button': 'Cadastrar'
    }
