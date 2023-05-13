

from django.urls import path

from pgms.views import View_Pgms_Available

app_name = "pgms"
urlpatterns = [
    path("", View_Pgms_Available.as_view(), name="scale-pgm"),
]

