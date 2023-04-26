from django.contrib import admin
from django.contrib.admin import register

from dataObjects.models import *


# Register your models here.

@register(Data_Objects)
class Data_ObjectsAdmin(admin.ModelAdmin):
    fields = ['name', 'brand', 'manufacturer', 'serial_num', 'status', 'type_obj', 'quantity', 'description']
    list_display = ['name', 'brand', 'manufacturer', 'serial_num', 'status', 'type_obj', 'quantity',  'description']
    search_fields = 'name', 'brand', 'manufacturer', 'serial_num', 'status', 'type_obj',
    list_filter = 'name', 'status', 'manufacturer', 'type_obj',
    list_per_page = 20
    ordering = '-id',


@register(Status_Obj)
class Status_ObjAdmin(admin.ModelAdmin):
    ordering = '-id',
    fields = ['title', 'local', 'last_user', 'qty_used', 'date_out', 'date_arrived', 'obj']
    list_display = ['title', 'local', 'last_user', 'qty_used', 'date_out', 'date_arrived', 'obj']
    readonly_fields = 'date_out', 'date_arrived',
    list_per_page = 20
