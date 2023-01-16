from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from clients.models import Client
from leads.models import Lead
from teams.models import Team


def index(request):
    return render(request, "homepage.html")


def about(request):
    return render(request, "about.html")


@login_required
def dashboard_view(request):
    team = Team.objects.filter(created_by=request.user).first()
    clients = Client.objects.filter(team=team).order_by("-created_at")[0:5]
    leads = Lead.objects.filter(team=team, converted_to_client=False).order_by(
        "-created_by"
    )[0:5]

    total_clients = Client.objects.filter(team=team).count()
    total_leads = Lead.objects.filter(team=team, converted_to_client=False).count()

    context = {
        "clients": clients,
        "leads": leads,
        "team": team,
        "total_clients": total_clients,
        "total_leads": total_leads,
    }
    return render(request, "dashboards/dashboard.html", context)
