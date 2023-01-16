from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("detail/", views.my_account_details_view, name="account_detail"),
    path("login/", views.AccountLoginView.as_view(), name="login"),
    path("logout/", views.AccountLogoutView.as_view(), name="logout"),
]
