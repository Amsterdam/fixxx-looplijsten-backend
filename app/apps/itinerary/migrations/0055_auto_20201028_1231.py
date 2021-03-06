# Generated by Django 3.1 on 2020-10-28 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0017_stadiumlabel"),
        ("itinerary", "0054_remove_itineraryitem_checked"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itinerarysettings",
            name="exclude_stadia",
            field=models.ManyToManyField(
                blank=True,
                related_name="settings_as_exclude_stadia",
                to="cases.Stadium",
            ),
        ),
        migrations.AlterField(
            model_name="itinerarysettings",
            name="secondary_stadia",
            field=models.ManyToManyField(
                blank=True,
                related_name="settings_as_secondary_stadia",
                to="cases.Stadium",
            ),
        ),
    ]
