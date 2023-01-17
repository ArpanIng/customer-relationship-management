from django import forms

from .models import Lead, Comment


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


class LeadAddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "cols": 10}),
        }
