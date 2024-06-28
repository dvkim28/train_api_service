# Generated by Django 4.2.13 on 2024-06-27 21:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("train_station", "0004_alter_route_unique_together_route_station_route"),
    ]

    operations = [
        migrations.AlterField(
            model_name="train",
            name="train_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="train_station.traintype",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("cargo", "seat", "journey", "order")},
        ),
    ]
