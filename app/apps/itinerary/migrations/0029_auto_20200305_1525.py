# Generated by Django 2.2.10 on 2020-03-05 15:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("itinerary", "0028_auto_20200305_1455"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itineraryteammember",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                related_query_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="itineraryteammember",
            unique_together={("user", "itinerary")},
        ),
    ]
