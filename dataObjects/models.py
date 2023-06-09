from datetime import datetime

from django.contrib.auth.models import User

from django.db import models
from django.db.models import Q


class Manager(models.Manager):

    def get_big_data(self, search):
        """ THIS WILL SEPARATE EACH REQUEST, RETUNING HIS VALUES BY ID REQUESTS_TO_OUT """
        data = None
        try:
            search = int(search)
            if search != " " and search is not None:
                all_req = Requests_To_Out.objects.all().filter(id=search).order_by('-id') \
                    .values_list('id', flat=True).prefetch_related("Status_Obj", "Data_Objects")  # get just id's
            else:
                all_req = Requests_To_Out.objects.all().order_by('-id').values_list('id', flat=True).prefetch_related(
                    "Status_Obj", "Data_Objects")  # get just id's
        except (ValueError, TypeError) as e:
            print(e)
            all_req = Requests_To_Out.objects.all().order_by('-id').values_list('id', flat=True) # get just id's

        formato_string = "%Y-%m-%d"

        try:
            data = datetime.strptime(search, formato_string)

        except (ValueError, TypeError) as e:
            print("A string não é uma data válida no formato DD/MM/AAAA.", e)

        qs1 = []
        for id_num in all_req:

            if len(qs1) > 0:
                queryset = Status_Obj.objects.filter(id_os=id_num)
                if data is not None:
                    queryset = queryset.filter(Q(date_out__date__gte=data) & Q(date_arrived__date__lte=data))
                if len(queryset) > 0:
                    is_available = queryset[0].date_out.strftime('%Y-%m-%d %H:%M:%S') == queryset[
                        0].date_arrived.strftime('%Y-%m-%d %H:%M:%S')
                    qs1.append({'id': id_num, 'values': queryset, 'is_available': is_available,
                                'description': queryset[0].id_os.description})


            else:
                queryset = Status_Obj.objects.filter(id_os=id_num)

                if data is not None:
                    queryset = queryset.filter(Q(date_out__date__gte=data) & Q(date_arrived__date__lte=data))
                if len(queryset) > 0:
                    is_available = queryset[0].date_out.strftime('%Y-%m-%d %H:%M:%S') == queryset[
                        0].date_arrived.strftime('%Y-%m-%d %H:%M:%S')
                    qs1 = [{'id': id_num,
                            'values': queryset,
                            'is_available': is_available,
                            'description': queryset[0].id_os.description}]

        return qs1


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


class Requests_To_Out(models.Model):
    objects = Manager()

    title = models.CharField(max_length=150, verbose_name="Titulo")
    local = models.CharField(max_length=255, blank=True, null=True, verbose_name="Local de utilização")
    doc_out = models.CharField(max_length=255, verbose_name="Caminho do arquivo")
    description = models.TextField(verbose_name="Descrição", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Solicitação de Saida"
        verbose_name_plural = "Solicitações de Saida"


class Status_Obj(models.Model):
    objects = Manager()
    id_os = models.ForeignKey(Requests_To_Out, on_delete=models.CASCADE)
    last_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Responsavel')
    qty_used = models.IntegerField(null=True, blank=True, verbose_name="Quantidade usada")
    date_out = models.DateTimeField(auto_now_add=True, verbose_name="Data de Saida")
    date_arrived = models.DateTimeField(auto_now=True, verbose_name="Data de Retorno")
    obj = models.ForeignKey(Data_Objects, on_delete=models.SET_NULL, null=True, verbose_name="Equipamento")

    #
    def __str__(self):
        return f"{self.id_os.title}"

    class Meta:
        verbose_name = "Histórico do Material"
        verbose_name_plural = "Histórico dos Materiais"
