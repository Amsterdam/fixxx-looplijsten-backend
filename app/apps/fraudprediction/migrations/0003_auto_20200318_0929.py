# Generated by Django 2.2.10 on 2020-03-18 09:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("fraudprediction", "0002_fraudprediction_synch_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="fraudprediction",
            old_name="synch_date",
            new_name="sync_date",
        ),
    ]
