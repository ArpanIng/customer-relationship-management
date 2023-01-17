from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect, get_object_or_404

from .forms import LeadCreateForm, LeadAddCommentForm
from .models import Lead, Comment

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
        self.lead = form.save(commit=False)
        self.lead.created_by = self.request.user
        self.lead.save()
        messages.success(self.request, "Lead created sucessfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user).first()
        context["lead_count"] = team.leads.count()
        context["max_leads"] = team.plan.max_leads
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lead
    context_object_name = "lead"
    template_name = "leads/lead_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LeadAddCommentForm()
        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lead
    form_class = LeadCreateForm
    context_object_name = "lead"
    template_name = "leads/lead_update.html"

    def form_valid(self, form):
        messages.success(self.request, "Lead updated sucessfully!")
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)


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


class AddCommentView(LoginRequiredMixin, generic.FormView):
    model = Comment
    form_class = LeadAddCommentForm
    template_name = "leads/lead_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user).first()
        comment = form.save(commit=False)
        comment.team = team
        comment.created_by = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        lead = self.get_object()
        return reverse("leads:lead_detail", kwargs={"pk": lead.pk})


class LeadConvertToClientView(LoginRequiredMixin, generic.View):
    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get("pk")
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
        return redirect("clients:client_list")
