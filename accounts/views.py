from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import UserProfile

from teams.models import Team


def signup_view(request):

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, "Account created successfully!")
            return redirect("accounts:login")
    else:
        form = UserCreationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


@login_required
def my_account_details_view(request):
    team = Team.objects.filter(created_by=request.user).first()
    context = {
        "team": team,
    }
    return render(request, "accounts/my_account_detail.html", context)


class AccountLoginView(views.LoginView):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        """Block authenticated user from accessing login URL."""
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class AccountLogoutView(views.LogoutView):
    template_name = "accounts/logout.html"
