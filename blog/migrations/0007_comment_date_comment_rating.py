# Generated by Django 4.2.11 on 2024-04-09 17:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="date",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="rating",
            field=models.IntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
    ]
