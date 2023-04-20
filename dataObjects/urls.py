from django.conf.urls.static import static

from WareHouse import settings
from .views import *
from django.urls import path

app_name = "dataObjects"
urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("out-obj/", Out_Obj.as_view(), name="out-obj"),
    path("register/", Register.as_view(), name="register"),
    path("extern-request/", Extern_Request.as_view(), name="extern-request"),
    path("scale-funcs/", Scale_Funcs.as_view(), name="scale-funcs"),
    path("communicate/", Communicate.as_view(), name="communicate"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
