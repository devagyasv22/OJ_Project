from django.urls import path
from . import views

urlpatterns = [
    path('', views.contest_list, name='contest_list'),
]
