# Generated by Django 4.2.11 on 2024-04-05 11:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hangman", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hangmangame",
            name="display",
            field=models.CharField(default="", max_length=50),
        ),
    ]
