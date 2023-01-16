from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LeadCreateForm
from .models import Lead

from clients.models import Client
from teams.models import Team


class LeadListView(LoginRequiredMixin, generic.ListView):
    model = Lead
    context_object_name = "leads"
    template_name = "leads/lead_list.html"

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, converted_to_client=False)


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    model = Lead
    form_class = LeadCreateForm
    context_object_name = "team"
    template_name = "leads/lead_create.html"

    def form_valid(self, form):
        # team = Team.objects.filter(created_by=self.request.user).first()
        self.lead = form.save(commit=False)
        self.lead.created_by = self.request.user
        # self.lead.team = team
        self.lead.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user).first()
        context["lead_count"] = team.leads.count()
        context["max_leads"] = team.plan.max_leads
        return context

    def get_success_url(self):
        messages.success(self.request, "Lead created sucessfully!")
        return reverse("leads:lead_list")


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lead
    context_object_name = "lead"
    template_name = "leads/lead_detail.html"

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)


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


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lead
    context_object_name = "lead"
    template_name = "leads/lead_update.html"


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Lead
    context_object_name = "lead"
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Lead deleted sucessfully!")
        return reverse("leads:lead_list")

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)


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
