from django.contrib.auth.models import User

from django.db import models


class Manager(models.Manager):
    pass


class Data_Objects(models.Model):
    objects = Manager()
    name = models.CharField(max_length=100, verbose_name="Nome", null=False)
    brand = models.CharField(max_length=255, verbose_name="Marca")
    manufacturer = models.CharField(max_length=255, verbose_name="Fabricante")
    status = models.CharField(max_length=20, verbose_name="Situação", null=True)
    quantity = models.IntegerField(verbose_name="Quantidade", default=1, null=True)
    serial_num = models.SlugField(verbose_name="Numero de Série", null=True)
    type_obj = models.CharField(max_length=255, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descrição")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Objeto"
        verbose_name_plural = "Objetos"


class Status_Obj(models.Model):
    id_os = models.IntegerField(verbose_name="ID OS")
    title = models.CharField(max_length=150, verbose_name="Titulo")
    local = models.CharField(max_length=255, blank=True, null=True, verbose_name="Local de utilização")
    last_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Responsavel')
    qty_used = models.IntegerField(null=True, blank=True, verbose_name="Quantidade usada")
    date_out = models.DateTimeField(auto_now_add=True, verbose_name="Data de Saida")
    date_arrived = models.DateTimeField(auto_now=True, verbose_name="Data de Retorno")
    obj = models.ForeignKey(Data_Objects, on_delete=models.SET_NULL, null=True, verbose_name="Equipamento")

    def __str__(self):
        return f"{self.title}, usados: {self.qty_used}"

    class Meta:
        verbose_name = "Status dos Materiais"
        verbose_name_plural = "Status dos Materiais"
