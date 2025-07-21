from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def dashboard_view(request):
    return render(request,"dashboard.html")

@login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required
def problem_set_view(request):
    return render(request, "problem_set.html")

@login_required
def contest_view(request):
    return render(request, "contest.html")

@login_required
def community_view(request):
    return render(request, "community.html")