# Generated by Django 4.2.13 on 2024-06-25 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_crew_managers_alter_crew_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crew",
            name="username",
            field=models.CharField(
                max_length=150, unique=True, verbose_name="username"
            ),
        ),
    ]
