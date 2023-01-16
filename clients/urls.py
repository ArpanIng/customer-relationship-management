from django.urls import path
from . import views

app_name = "clients"
urlpatterns = [
    path("", views.client_list_view, name="client_list"),
    path("add/", views.client_create_view, name="client_create"),
    path("<int:pk>/", views.client_detail_view, name="client_detail"),
    path("<int:pk>/update/", views.client_update_view, name="client_update"),
    path("<int:pk>/delete/", views.client_delete_view, name="client_delete"),
]
