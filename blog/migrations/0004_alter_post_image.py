# Generated by Django 4.2.11 on 2024-04-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_post_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(null=True, upload_to="static/posts"),
        ),
    ]