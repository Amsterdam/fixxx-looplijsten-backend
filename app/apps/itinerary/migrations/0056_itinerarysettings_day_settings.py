# Generated by Django 3.1.2 on 2020-11-17 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planner", "0011_daysettings"),
        ("itinerary", "0055_auto_20201028_1231"),
    ]

    operations = [
        migrations.AddField(
            model_name="itinerarysettings",
            name="day_settings",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="itinerary_day_settings",
                to="planner.daysettings",
            ),
        ),
    ]
