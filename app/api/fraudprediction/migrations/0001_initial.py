# Generated by Django 2.2.10 on 2020-03-17 13:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FraudPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(max_length=255, null=True, unique=True)),
                ('fraud_probability', models.FloatField()),
                ('fraud_prediction', models.BooleanField()),
                ('business_rules', django.contrib.postgres.fields.jsonb.JSONField()),
                ('shap_values', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
