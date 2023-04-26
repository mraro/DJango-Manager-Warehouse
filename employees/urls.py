
from dataObjects.views import Home
from employees.views import Login_Employees, Logout_Employees, Register_Employees
from django.urls import path

app_name = "employees"
urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login/", Login_Employees.as_view(), name="login"),
    path("logout/", Logout_Employees.as_view(), name="logout"),
    path("register/", Register_Employees.as_view(), name="register"),

]

