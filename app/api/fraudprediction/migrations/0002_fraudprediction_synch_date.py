# Generated by Django 2.2.10 on 2020-03-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fraudprediction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fraudprediction',
            name='synch_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
