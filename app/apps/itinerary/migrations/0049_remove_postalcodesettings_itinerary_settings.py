# Generated by Django 3.0.7 on 2020-07-06 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("itinerary", "0048_auto_20200706_1212"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postalcodesettings",
            name="itinerary_settings",
        ),
    ]
