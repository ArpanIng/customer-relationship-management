from django.urls import path
from . import views

app_name = "leads"
urlpatterns = [
    path("", views.LeadListView.as_view(), name="lead_list"),
    path("add/", views.LeadCreateView.as_view(), name="lead_create"),
    path("<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"),
    path("<int:pk>/update/", views.lead_update_view, name="lead_update"),
    path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name="lead_delete"),
    path("<int:pk>/convert/", views.convert_to_client_view, name="lead_convert"),
]
