from django.contrib import admin
from django.contrib.admin import register

from dataObjects.models import *


# Register your models here.

@register(Data_Objects)
class Data_ObjectsAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'brand', 'manufacturer', 'serial_num', 'status', 'type_obj', 'quantity', 'description']
    list_display = ['id', 'name', 'brand', 'manufacturer', 'serial_num', 'status', 'type_obj', 'quantity',  'description']
    search_fields = 'name', 'brand', 'manufacturer', 'serial_num', 'status', 'type_obj',
    list_filter = 'name', 'status', 'manufacturer', 'type_obj',
    list_per_page = 20
    ordering = '-id',
    list_editable = ['quantity',]


@register(Status_Obj)
class Status_ObjAdmin(admin.ModelAdmin):
    ordering = '-id',
    fields = ['id', 'id_os', 'last_user', 'qty_used', 'date_out', 'date_arrived', 'obj']
    list_display = ['id', 'id_os',  'last_user', 'qty_used', 'date_out', 'date_arrived', 'obj']
    search_fields = 'id_os', 'last_user'
    list_filter = 'id_os', 'last_user'
    readonly_fields = 'date_out', 'date_arrived',
    list_per_page = 20


@register(Requests_To_Out)
class Requests_To_OutAdmin(admin.ModelAdmin):
    ordering = '-id',
    fields = 'id', 'title', 'local', 'description'
    list_display = 'id', 'title', 'local', 'doc_out', 'description'
    search_fields = 'id', 'title',  'local',

