# Generated by Django 2.1.11 on 2019-11-19 21:26

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Case",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stadion", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("postal_code", models.CharField(max_length=6)),
                ("stadium", models.CharField(max_length=255)),
            ],
        ),
    ]
