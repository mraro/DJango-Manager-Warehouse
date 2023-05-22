from django import forms
from django.forms.widgets import Input

from pgms.models import *
from utils import add_placeholder, add_attr


class Form_PGM_add_Employees(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['showman'], "Nome do Apresentador")
        add_placeholder(self.fields['camera_men'], "Nome do Camera Men")
        add_placeholder(self.fields['scenographer'], "Nome do responsável pelo Cenario")
        add_placeholder(self.fields['audio_men'], "Nome do operador de audio")
        add_placeholder(self.fields['microphone_men'], "Nome de quem coloca o microfone nos convidados")
        add_placeholder(self.fields['producer'], "Nome do Produtor responsavel")
        add_placeholder(self.fields['reporter'], "Nome do Reporter")
        add_placeholder(self.fields['journalist'], "Nome do Jornalista")
        add_placeholder(self.fields['director_img'], "Nome do Diretor de Imagem")

    showman = forms.CharField(max_length=255, label="Apresentador", required=True)
    camera_men = forms.CharField(max_length=255, label="Camera Men")
    scenographer = forms.CharField(max_length=255, label="Cenógrafo")
    audio_men = forms.CharField(max_length=255, label="Sonoplasta")
    microphone_men = forms.CharField(max_length=255, label="Aux. Microfonagem")
    producer = forms.CharField(max_length=255, label="Produtor Responsavel", required=True)
    reporter = forms.CharField(max_length=255, label="Reporter")
    journalist = forms.CharField(max_length=255, label="Jornalista")

#
    class Meta:
        model = Programs_Show
        # exclude = "id",
        fields = "pgm", "showman", "camera_men", "scenographer", "audio_men", "microphone_men", "producer", \
            "reporter", "journalist", "director_img",


class Form_PGM(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['name'], 'Adicione o Nome do Programa')
        add_attr(self.fields['img_pgm'], 'onchange', 'previewImagem()')

    class Meta:
        model = Program_Product
        fields = 'name', 'img_pgm'

    name = forms.CharField(max_length=255, label="Nome", required=True)
    img_pgm = forms.ImageField(required=True, label="Fundo")

    # to_show = forms.DateTimeField(
    #     label='Data de Começo',
    #     # widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'flatpickr'}, format=['%d/%m/%y - %H:%M']),
    #     input_formats=['%d/%m/%y - %H:%M'])
