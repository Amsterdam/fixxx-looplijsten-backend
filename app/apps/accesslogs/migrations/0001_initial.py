# Generated by Django 2.1.15 on 2020-01-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogEntry",
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
                ("request_user_email", models.CharField(max_length=255, null=True)),
                ("request_user_id", models.CharField(max_length=255, null=True)),
                ("request_uri", models.CharField(max_length=255)),
                ("request_meta", models.TextField()),
                ("response_status_code", models.CharField(max_length=3)),
            ],
        ),
    ]
