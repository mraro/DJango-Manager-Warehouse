# Generated by Django 4.1.5 on 2023-04-29 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataObjects", "0012_alter_status_obj_id_os"),
    ]

    operations = [
        migrations.AlterField(
            model_name="status_obj",
            name="id_os",
            field=models.IntegerField(verbose_name="ID OS"),
        ),
    ]
