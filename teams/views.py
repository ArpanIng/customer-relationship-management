from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TeamEditForm
from .models import Team


@login_required
def edit_team_view(request, pk):
    team = get_object_or_404(Team, created_by=request.user, id=pk)
    if request.method == "POST":
        form = TeamEditForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team edited successfully!")
            return redirect("accounts:account_detail")
    else:
        form = TeamEditForm(instance=team)

    context = {
        "form": form,
        "team": team,
    }
    return render(request, "teams/team_edit.html", context)
