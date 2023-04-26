from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils import add_placeholder, name_validator, password_validator


class Reg_Emp_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Nome de usuario para login')
        add_placeholder(self.fields['first_name'], 'Nome')
        add_placeholder(self.fields['last_name'], 'Sobrenome')

    first_name = forms.CharField(validators=[name_validator],
                                 min_length=4,
                                 max_length=150,
                                 label='Primeiro nome',
                                 )

    last_name = forms.CharField(min_length=4,
                                max_length=150,
                                label='Sobrenome',
                                )

    username = forms.CharField(min_length=4,
                               max_length=150,
                               label='Nome de Usuario',
                               )  # THIS WORKS BETTER THAN add_attr(self.fields['username'],
    # 'min_length', '3')
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha',
        }),
        error_messages={
            'required': "A Senha não pode ser vazia"
        },
        validators=[password_validator],
        help_text=(
            'A senha deve conter caracters especiais, letras maiusculas e minusculas alem de numeros'
            ' com pelo menos 8 caracteres'
        ),
        label='Senha',
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita a senha'
        }),
        error_messages={
            'required': "A Senha não pode ser vazia"
        },
        label='Verifique a senha'

    )

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')  # THIS CLEANED_DATA WAS CHECKED BY DJANGO
        # data = self.clean # THIS IS DIRECT WITHOUT DJANGO VALIDATOR
        if 'root' in data:
            raise ValidationError(
                f'{"Nome proibido"}: %(value)s',
                code='invalid',
                params={'value': 'root'}
            )
        return data

    def clean(self):  # DEFINED IN SUPER CLASS
        data_cleaned = super().clean()
        password = data_cleaned.get('password')  # GET VALUES FROM INPUT VALIDATION
        password2 = data_cleaned.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': 'Senhas divergentes'  # SET MESSAGE AND WHERE SHOULD SHOW

            },
                code='invalid'
            )  # IT'S POSSIBLE SEND A LIST OF PROBLEMS

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
        ]

        error_messages = {
            'username': {
                'required': "Não pode ser vazio",
            }
        }
