from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form

from dataObjects.models import Data_Objects

from utils import add_placeholder


class Create_Obj(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['name'], "Digite o nome do material") # noqa
        add_placeholder(self.fields['brand'], "Digite o modelo ou tipo do material") # noqa
        add_placeholder(self.fields['manufacturer'], "Digite o nome do fabricante") # noqa
        add_placeholder(self.fields['serial_num'], "Digite apenas numeros e letras para o S/N:") # noqa
        add_placeholder(self.fields['description'], "Digite uma breve descrição do que é, para oque serve...") # noqa

    class Meta:
        model = Data_Objects
        fields = ['name', 'brand', 'manufacturer', 'serial_num', 'type_obj', 'quantity', 'description']

    name = forms.CharField(required=True, label="Nome") # noqa
    brand = forms.CharField(label="Modelo", required=False) # noqa
    manufacturer = forms.CharField(label="Fabricante", required=False) # noqa
    serial_num = forms.CharField(label='S/N: ', required=False) # noqa
    quantity = forms.IntegerField(label='Quantidade', min_value=1, required=False) # noqa
    description = forms.CharField(label='Descrição do equipamento', widget=forms.Textarea, required=False) # noqa
    type_obj = forms.CharField(label='Status',
                               help_text=(
                                   "Reutilizavel para equipamentos que devem voltar e descartavel serão aqueles que "   # noqa
                                   "é de uso unico, tais como as pilhas"), # noqa
                               widget=forms.Select(
                                   choices=(
                                       ('UNIC', 'Reutilizável'), # noqa
                                       ('MULT', 'Descartavel'), # noqa
                                   )
                               ))

    def clean_serial_num(self):
        serial = self.cleaned_data.get('serial_num')
        if serial == "":
            return serial
        exist = Data_Objects.objects.filter(serial_num=serial).exists()
        if exist:
            raise ValidationError("Esse numero de série ja existe")
        return serial
