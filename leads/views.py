from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LeadCreateForm
from .models import Lead

from clients.models import Client
from teams.models import Team


class LeadListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "leads"
    template_name = "leads/lead_list.html"

    def get_queryset(self):
        return Lead.objects.filter(
            created_by=self.request.user, converted_to_client=False
        )


@login_required
def lead_create_view(request):

    team = Team.objects.filter(created_by=request.user).first()
    lead_count = team.leads.count()
    max_leads = team.plan.max_leads

    if request.method == "POST":
        form = LeadCreateForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()
            messages.success(request, "Lead created sucessfully!")
            return redirect("leads:lead_list")
    else:
        form = LeadCreateForm()

    context = {
        "form": form,
        "team": team,
        "lead_count": lead_count,
        "max_leads": max_leads,
    }
    return render(request, "leads/lead_create.html", context)


@login_required
def lead_detail_view(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, id=pk)

    context = {
        "lead": lead,
    }
    return render(request, "leads/lead_detail.html", context)


@login_required
def lead_update_view(request, pk):

    lead = get_object_or_404(Lead, created_by=request.user, id=pk)

    if request.method == "POST":
        form = LeadCreateForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead updated sucessfully!")
            return redirect("leads:lead_detail", lead.pk)
    else:
        form = LeadCreateForm(instance=lead)

    context = {
        "lead": lead,
        "form": form,
    }
    return render(request, "leads/lead_update.html", context)


@login_required
def lead_delete_view(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, id=pk)

    if request.method == "POST":
        lead.delete()
        messages.success(request, "Lead deleted sucessfully!")
        return redirect("leads:lead_list")

    context = {
        "lead": lead,
    }
    return render(request, "leads/lead_delete.html", context)


@login_required
def convert_to_client_view(request, pk):

    lead = get_object_or_404(Lead, created_by=request.user, id=pk)
    team = Team.objects.filter(created_by=request.user).first()

    Client.objects.create(
        team=team,
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
    )
    lead.converted_to_client = True
    lead.save()
    messages.success(request, "Lead converted to client sucessfully!")
    return redirect("leads:lead_list")
