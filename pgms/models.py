from django.db import models


class Program_Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    img_pgm = models.ImageField(upload_to='media/covers/',
                                blank=True,
                                default='static/img/default.jpg', verbose_name="Fundo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produção"
        verbose_name_plural = "Produções"


class Programs_Show(models.Model):
    pgm = models.ForeignKey(Program_Product, on_delete=models.SET_NULL, null=True)
    showman = models.CharField(max_length=255, verbose_name="Apresentador")
    camera_men = models.CharField(max_length=255, verbose_name="Camera Man")
    scenographer = models.CharField(max_length=255, verbose_name="Cenógrafo")
    audio_men = models.CharField(max_length=255, verbose_name="Sonoplasta")
    microphone_men = models.CharField(max_length=255, verbose_name="Aux. Microfone")
    producer = models.CharField(max_length=255, verbose_name="Produtor Responsavel")
    reporter = models.CharField(max_length=255, verbose_name="Reporter")
    journalist = models.CharField(max_length=255, verbose_name="Jornalista")
    director_img = models.CharField(max_length=255, verbose_name="Diretor de Imagem")
    date_rec = models.DateField(null=True, blank=True, verbose_name="Data de Gravação")
    time_rec = models.TimeField(null=True, blank=True, verbose_name="Hora de Gravação")
    channel = models.CharField(max_length=50, verbose_name="Canal")

    date_made = models.DateTimeField(auto_now_add=True, verbose_name="Data de Saida")

    def __str__(self):
        return self.pgm.name

    class Meta:
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
