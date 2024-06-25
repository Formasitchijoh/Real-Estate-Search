# Generated by Django 5.0.6 on 2024-06-25 01:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listings", "0009_processedlistings_listing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="processedlistings",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="listings.listing"
            ),
        ),
    ]
