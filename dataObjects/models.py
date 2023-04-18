from django.contrib.auth.models import User

from django.db import models


class Manager(models.Manager):
    pass


class Status_Obj(models.Model):
    title = models.CharField(max_length=150)
    local = models.CharField(max_length=255)
    last_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    date_out = models.DateTimeField(auto_created=True)
    date_arrived = models.DateTimeField(auto_now_add=True)


class Data_Objects(models.Model):
    objects = Manager()
    name = models.CharField(max_length=100, verbose_name="Nome")
    brand = models.CharField(max_length=255, verbose_name="Marca")
    manufacturer = models.CharField(max_length=255, verbose_name="Fabricante")
    status = models.ForeignKey(Status_Obj, on_delete=models.SET_NULL, null=True)
    serial_num = models.SlugField(verbose_name="Numero de Série")
    type_obj = models.CharField(max_length=255, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descrição")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Objeto"
        verbose_name_plural = "Objetos"
