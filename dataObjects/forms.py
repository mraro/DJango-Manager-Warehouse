from django import forms
from django.forms import Form

from dataObjects.models import Data_Objects


class Create_Obj(forms.ModelForm):
    class Meta:
        model = Data_Objects
        fields = ['name', 'brand', 'manufacturer', 'serial_num', 'type_obj', 'quantity', 'description']

    name = forms.CharField(required=True, label="Nome")
    brand = forms.CharField(label="Modelo", required=False)
    manufacturer = forms.CharField(label="Fabricante", required=False)
    serial_num = forms.CharField(label='S/N: ', required=False)
    type_obj = forms.CharField(label='Tipo de Material', required=False)
    description = forms.CharField(label='Descrição do equipamento', widget=forms.Textarea, required=False)
    # status = forms.CharField(label='Status', widget=forms.Select(
    #                                                              choices=(
    #                                                                  ('O', 'Disponivel'),
    #                                                                  ('F', 'Funcionando'),
    #                                                                  ('D', 'Defeito'),
    #                                                                  ('U', 'Em uso'),
    #                                                                  ('M', 'Em Manutenção'),
    #                                                              )
    #                                                              ))
