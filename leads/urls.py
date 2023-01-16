from django.urls import path
from . import views

app_name = "leads"
urlpatterns = [
    path("", views.lead_list_view, name="lead_list"),
    path("add/", views.lead_create_view, name="lead_create"),
    path("<int:pk>/", views.lead_detail_view, name="lead_detail"),
    path("<int:pk>/update/", views.lead_update_view, name="lead_update"),
    path("<int:pk>/delete/", views.lead_delete_view, name="lead_delete"),
    path("<int:pk>/convert/", views.convert_to_client_view, name="lead_convert"),
]
