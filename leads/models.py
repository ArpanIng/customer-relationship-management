from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from teams.models import Team


class Lead(models.Model):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    CHOICES_PRIORITY = (
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    )

    NEW = "new"
    CONTACTED = "contacted"
    WON = "won"
    LOST = "lost"

    CHOICES_STATUS = (
        (NEW, "New"),
        (CONTACTED, "Contacted"),
        (WON, "Won"),
        (LOST, "Lost"),
    )

    team = models.ForeignKey(Team, related_name="leads", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=6, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=9, choices=CHOICES_STATUS, default=NEW)
    converted_to_client = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="leads", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def get_absolute_url(self):
        return reverse("leads:lead_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Comment(models.Model):
    team = models.ForeignKey(
        Team, related_name="lead_comments", on_delete=models.CASCADE
    )
    lead = models.ForeignKey(Lead, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="lead_comments", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
