# Generated by Django 4.1.5 on 2023-04-26 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dataObjects", "0007_remove_data_objects_status_status_obj_obj"),
    ]

    operations = [
        migrations.AddField(
            model_name="data_objects",
            name="status",
            field=models.CharField(max_length=20, null=True, verbose_name="Situação"),
        ),
    ]
