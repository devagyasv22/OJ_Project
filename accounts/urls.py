from django.urls import path
from django.urls import path, include

from .views import (
    SignUpView,
    dashboard_view,
    profile_view,
    problem_set_view,
    contest_view,
    community_view,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/", profile_view, name="profile"),
    path("problem-set/", problem_set_view, name="problem_set"),
    path("contest/", contest_view, name="contest"),
    path("community/", community_view, name="community"),
    path('compiler/',include('compiler.urls')),
]