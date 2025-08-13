from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render
from .models import UserProfile

from django.shortcuts import render, redirect
from .forms import ProfileForm
from .utils import get_cf_data
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def get_form(self, form_class=None):
    form = super().get_form(form_class)
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control bg-dark text-white border-secondary'
    return form


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request,"dashboard.html")

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    cf_data = get_cf_data(profile.codeforces_handle) if profile.codeforces_handle else None
    is_full_url = False
    if profile.codeforces_handle and profile.codeforces_handle.startswith("http"):
        is_full_url = True

    return render(request, "profile.html", {
        "profile": profile,
        "cf_data": cf_data,
        "is_full_url": is_full_url
    })




@login_required
def problem_set_view(request):
    return render(request, "problem_set.html")

@login_required
def contest_view(request):
    return render(request, "contest.html")

@login_required
def community_view(request):
    return render(request, "community.html")




# def profile_view(request):
#     profile = UserProfile.objects.get(user=request.user)
#     cf_data = get_cf_data(profile.codeforces_handle) if profile.codeforces_handle else None
#     return render(request, "profile.html", {
#         "profile": profile,
#         "cf_data": cf_data
#     })
