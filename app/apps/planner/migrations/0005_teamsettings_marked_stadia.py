# Generated by Django 3.1 on 2020-10-27 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0017_stadiumlabel"),
        ("planner", "0004_auto_20201019_1102"),
    ]

    operations = [
        migrations.AddField(
            model_name="teamsettings",
            name="marked_stadia",
            field=models.ManyToManyField(
                blank=True,
                related_name="stadium_label_team_settings_list",
                to="cases.StadiumLabel",
            ),
        ),
    ]
