from django import forms

from .models import Client


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "team",
            "first_name",
            "last_name",
            "email",
            "description",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "cols": 15}),
        }
