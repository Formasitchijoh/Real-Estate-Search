# Generated by Django 5.0.6 on 2024-06-22 06:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listings", "0002_rename_unnamed_0_processedlistings_unnamed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="processedlistings",
            name="query",
            field=models.CharField(default="", max_length=255),
        ),
    ]