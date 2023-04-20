from django.contrib import admin
from django.contrib.admin import register

from dataObjects.models import Data_Objects


# Register your models here.

@register(Data_Objects)
class Data_ObjectsAdmin(admin.ModelAdmin):
    fields = ['name', 'brand', 'manufacture', 'status', 'serial_num', 'type_obj', 'description']
    search_fields = 'name',
