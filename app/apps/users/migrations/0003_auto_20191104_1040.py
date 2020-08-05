# Generated by Django 2.1.9 on 2019-11-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_auto_20171227_2246"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="username",),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
