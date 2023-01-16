from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import ClientCreateForm
from .models import Client

from teams.models import Team


@login_required
def client_list_view(request):
    clients = Client.objects.filter(created_by=request.user)

    context = {
        "clients": clients,
    }
    return render(request, "clients/client_list.html", context)


@login_required
def client_create_view(request):

    team = Team.objects.filter(created_by=request.user).first()
    client_count = team.clients.count()
    max_clients = team.plan.max_clients

    if request.method == "POST":
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, "Client created sucessfully!")
            return redirect("clients:client_list")
    else:
        form = ClientCreateForm()

    context = {
        "team": team,
        "form": form,
        "client_count": client_count,
        "max_clients": max_clients,
    }
    return render(request, "clients/client_create.html", context)


@login_required
def client_detail_view(request, pk):
    client = get_object_or_404(Client, created_by=request.user, id=pk)

    context = {
        "client": client,
    }
    return render(request, "clients/client_detail.html", context)


@login_required
def client_update_view(request, pk):

    client = get_object_or_404(Client, created_by=request.user, id=pk)

    if request.method == "POST":
        form = ClientCreateForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated sucessfully!")
            return redirect("clients:client_detail", client.pk)
    else:
        form = ClientCreateForm(instance=client)

    context = {
        "client": client,
        "form": form,
    }
    return render(request, "clients/client_update.html", context)


@login_required
def client_delete_view(request, pk):
    client = get_object_or_404(Client, created_by=request.user, id=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Client deleted sucessfully!")
        return redirect("clients:client_list")

    context = {
        "client": client,
    }
    return render(request, "clients/client_delete.html", context)
