# Generated by Django 3.1 on 2020-09-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_auto_20200429_0932"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
