# Generated by Django 4.1.5 on 2023-01-16 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0002_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="plan",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="teams.plan",
            ),
            preserve_default=False,
        ),
    ]
