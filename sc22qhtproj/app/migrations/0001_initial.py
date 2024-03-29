# Generated by Django 4.2.10 on 2024-03-18 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Story",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("headline", models.CharField(max_length=64)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("pol", "Politics"),
                            ("art", "Art"),
                            ("tech", "Technology"),
                            ("trivia", "Trivia"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        choices=[
                            ("uk", "United Kingdom"),
                            ("eu", "European Union"),
                            ("w", "World"),
                        ],
                        max_length=10,
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("details", models.CharField(max_length=128)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.author"
                    ),
                ),
            ],
        ),
    ]
