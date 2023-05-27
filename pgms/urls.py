

from django.urls import path

from pgms.views import *

app_name = "pgms"
urlpatterns = [
    path("", View_Pgms.as_view(), name="scale-pgm"),
    path("view", View_Pgms_Available.as_view(), name="view-pgm"),
    path("add_pgm", View_Pgms_ADD.as_view(), name="add-pgm"),
    path("set_date", View_Pgms_Set_Days.as_view(), name="set-date"),
    path("save-setup-date", View_Pgms_Set_Days.as_view(), name="save-setup-date"),
]

