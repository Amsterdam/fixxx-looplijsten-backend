# Generated by Django 2.1.11 on 2019-12-03 16:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("itinerary", "0018_itineraryitem_position"),
    ]

    operations = [
        migrations.RemoveField(model_name="itineraryitem", name="position",),
    ]