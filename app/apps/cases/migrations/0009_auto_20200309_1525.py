# Generated by Django 2.2.10 on 2020-03-09 15:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("itinerary", "0034_itinerarysettings_target_itinerary_length"),
        ("cases", "0008_auto_20200309_1302"),
    ]

    operations = [
        migrations.RenameModel(old_name="State", new_name="Stadium",),
    ]
