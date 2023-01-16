from django import forms

from .models import Lead


class LeadCreateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "team",
            "first_name",
            "last_name",
            "email",
            "description",
            "priority",
            "status",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "cols": 15}),
        }
