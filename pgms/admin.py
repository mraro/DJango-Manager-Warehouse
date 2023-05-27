from django.contrib import admin

from pgms.models import *


@admin.register(Programs_Show)
class Admin_Programs_Show(admin.ModelAdmin):
    fields = "pgm", "showman", "camera_men", "scenographer", "audio_men", "microphone_men", "producer", "reporter", \
        "journalist", "director_img", "date_rec", "time_rec", "channel"

    list_display = "pgm", "showman", "camera_men", "scenographer", "audio_men", "microphone_men", "producer", \
        "reporter", "journalist", "director_img", "date_rec", "time_rec", "channel"
    list_per_page = 20
    ordering = "-id",


@admin.register(Program_Product)
class Admin_Program_Product(admin.ModelAdmin):
    fields = "name", "img_pgm"
    list_display = "name", "img_pgm"
    list_per_page = 20
    ordering = "-id",
