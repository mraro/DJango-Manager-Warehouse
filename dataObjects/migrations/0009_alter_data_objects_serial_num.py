# Generated by Django 4.1.5 on 2023-04-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataObjects", "0008_data_objects_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="data_objects",
            name="serial_num",
            field=models.SlugField(
                null=True, unique=True, verbose_name="Numero de Série"
            ),
        ),
    ]