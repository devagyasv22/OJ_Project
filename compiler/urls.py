from django.urls import path
from compiler import views

urlpatterns = [
    path("", views.submit_code, name="submit_code"),
    path("result/",views.result_page,name="result_page"),
]