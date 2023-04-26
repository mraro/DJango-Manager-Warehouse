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
    serial_num = models.SlugField(verbose_name="Numero de Série", unique=True, null=True)
    type_obj = models.CharField(max_length=255, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descrição")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Objeto"
        verbose_name_plural = "Objetos"


class Status_Obj(models.Model):
    title = models.CharField(max_length=150)
    local = models.CharField(max_length=255, blank=True, null=True)
    last_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    qty_used = models.IntegerField(null=True, blank=True)
    date_out = models.DateTimeField(auto_now_add=True)
    date_arrived = models.DateTimeField(auto_now=True)
    obj = models.ForeignKey(Data_Objects, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title}, usados: {self.qty_used}"
