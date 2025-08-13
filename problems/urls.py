from django.urls import path
from . import views
from .views import ai_review_code 
from .views import problem_detail

urlpatterns = [
    # path('',                         problem_list,   name='problem_list'),
    path('<int:problem_id>/',        problem_detail, name='problem_detail'),
    path('', views.problem_list, name='problem_list'),
    path('<int:problem_id>/submit/', views.submit_code, name='submit_code'),
    path("problems/<int:problem_id>/ai-review/", ai_review_code, name="ai_review_code"),

]
