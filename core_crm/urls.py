from django.contrib import admin
from django.urls import include, path
from dashboards.views import index, about

urlpatterns = [
    path("", index, name="homepage"),
    path("about/", about, name="about"),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("client/", include("clients.urls")),
    path("dashboard/", include("dashboards.urls")),
    path("team/", include("teams.urls")),
    path("lead/", include("leads.urls")),
]
