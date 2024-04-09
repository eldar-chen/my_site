# Generated by Django 4.2.11 on 2024-04-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_alter_post_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="image_name",
        ),
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(null=True, upload_to="posts"),
        ),
    ]
