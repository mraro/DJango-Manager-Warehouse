# Generated by Django 4.1.5 on 2023-04-25 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dataObjects", "0006_alter_status_obj_qty_used"),
    ]

    operations = [
        migrations.RemoveField(model_name="data_objects", name="status",),
        migrations.AddField(
            model_name="status_obj",
            name="obj",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="dataObjects.data_objects",
            ),
        ),
    ]
