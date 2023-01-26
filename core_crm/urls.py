from django.contrib import admin
from django.urls import include, path
from dashboards.views import index, about

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),  # django_tailwind
    path("", index, name="homepage"),
    path("about/", about, name="about"),
    path("account/", include("accounts.urls")),
    path("client/", include("clients.urls")),
    path("dashboard/", include("dashboards.urls")),
    path("team/", include("teams.urls")),
    path("lead/", include("leads.urls")),
]
