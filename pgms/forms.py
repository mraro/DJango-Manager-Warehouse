from django import forms

from pgms.models import *
from utils import add_placeholder


class Form_PGM_add_Employees(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         add_placeholder(self.fields['name'], "Nome do Programa")
#         add_placeholder(self.fields['showman'], "Nome do Apresentador")
#         add_placeholder(self.fields['camera_men'], "Nome do Camera Men")
#         add_placeholder(self.fields['scenographer'], "Nome do responsável pelo Cenario")
#         add_placeholder(self.fields['audio_men'], "Nome do operador de audio")
#         add_placeholder(self.fields['microphone_men'], "Nome de quem coloca o microfone nos convidados")
#         add_placeholder(self.fields['producer'], "Nome do Produtor responsavel")
#         add_placeholder(self.fields['reporter'], "Nome do Reporter")
#         add_placeholder(self.fields['journalist'], "Nome do Jornalista")
#         add_placeholder(self.fields['director_img'], "Nome do Diretor de Imagem")
#
#     name = forms.CharField(max_length=255, label="Nome", required=True)
#     showman = forms.CharField(max_length=255, label="Apresentador", required=True)
#     camera_men = forms.CharField(max_length=255, label="Camera Men")
#     scenographer = forms.CharField(max_length=255, label="Cenógrafo")
#     audio_men = forms.CharField(max_length=255, label="Sonoplasta")
#     microphone_men = forms.CharField(max_length=255, label="Aux. Microfonagem")
#     producer = forms.CharField(max_length=255, label="Produtor Responsavel", required=True)
#     reporter = forms.CharField(max_length=255, label="Reporter")
#     journalist = forms.CharField(max_length=255, label="Jornalista")
#     director_img = forms.CharField(max_length=255, label="Diretor de Imagem")

#
    class Meta:
        model = Program_Product
        exclude = "id",
#         fields = "name", "showman", "camera_men", "scenographer", "audio_men", "microphone_men", "producer", \
#             "reporter", "journalist", "director_img", "img_pgm",


class Form_PGM(forms.ModelForm):
    class Meta:
        model = Program_Product
        exclude = "id",

    name = forms.CharField(max_length=255, label="Nome", required=True)
    img_pgm = forms.ImageField(required=True, label="Fundo")
    # to_show = forms.CharField(widget=forms.DateTimeField)