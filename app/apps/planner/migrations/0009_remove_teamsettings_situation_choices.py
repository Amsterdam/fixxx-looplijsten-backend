# Generated by Django 3.1.2 on 2020-11-11 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("planner", "0008_postalcoderange_postalcoderangeset"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teamsettings",
            name="situation_choices",
        ),
    ]
