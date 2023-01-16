from django.db import models
from django.contrib.auth.models import User

from teams.models import Team


class Client(models.Model):
    team = models.ForeignKey(Team, related_name="clients", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="clients", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
