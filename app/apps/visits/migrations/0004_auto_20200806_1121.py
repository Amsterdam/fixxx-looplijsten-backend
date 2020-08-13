# Generated by Django 3.0.7 on 2020-08-06 11:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0003_auto_20200724_1528"),
    ]

    operations = [
        migrations.RemoveField(model_name="visit", name="cooperation",),
        migrations.RemoveField(model_name="visit", name="cooperation_likely_fraud",),
        migrations.RemoveField(model_name="visit", name="no_cooperation",),
        migrations.RemoveField(
            model_name="visit", name="no_cooperation_hotel_furnished",
        ),
        migrations.RemoveField(
            model_name="visit", name="no_cooperation_likely_inhabited",
        ),
        migrations.RemoveField(
            model_name="visit", name="no_cooperation_malfunctioning_doorbell",
        ),
        migrations.RemoveField(model_name="visit", name="no_cooperation_vacant",),
        migrations.RemoveField(model_name="visit", name="no_cooperation_video_call",),
        migrations.RemoveField(model_name="visit", name="nobody_present",),
        migrations.RemoveField(model_name="visit", name="suggest_discontinue_case",),
        migrations.RemoveField(model_name="visit", name="suggest_next_visit_day",),
        migrations.RemoveField(model_name="visit", name="suggest_next_visit_evening",),
        migrations.RemoveField(model_name="visit", name="suggest_next_visit_unknown",),
        migrations.RemoveField(model_name="visit", name="suggest_next_visit_weekend",),
        migrations.AddField(
            model_name="visit",
            name="observations",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("malfunctioning_doorbell", "Bel functioneert niet"),
                        ("video_call", "Contact via videobel"),
                        ("hotel_furnished", "Hotelmatig ingericht"),
                        ("vacant", "Leegstaand"),
                        ("likely_inhabited", "Vermoedelijk bewoond"),
                    ],
                    max_length=50,
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="visit",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("nobody_present", "Niemand aanwezig"),
                    ("no_cooperation", "Geen medewerking"),
                    ("access_granted", "Toegang verleend"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="visit",
            name="suggest_next_visit",
            field=models.CharField(
                choices=[
                    ("weekend", "Weekend"),
                    ("daytime", "Overdag"),
                    ("evening", "'s Avonds"),
                    ("unknown", "Onbekend"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="visit",
            name="suggest_visit_next_time",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="visit", name="description", field=models.TextField(null=True),
        ),
    ]