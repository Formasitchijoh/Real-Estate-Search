# Generated by Django 4.2.7 on 2024-07-25 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Listing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("link", models.URLField()),
                ("listing_type", models.CharField(max_length=100)),
                ("bedroom", models.FloatField()),
                ("bathrooms", models.FloatField()),
                ("location", models.CharField(max_length=255)),
                ("town", models.CharField(max_length=255)),
                ("price", models.FloatField()),
                ("pricepermonth", models.CharField(max_length=500)),
                ("views", models.IntegerField()),
                ("reactions", models.IntegerField()),
            ],
            options={
                "db_table": "listings",
            },
        ),
        migrations.CreateModel(
            name="Query",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("query", models.CharField(default="", max_length=1000)),
            ],
            options={
                "db_table": "querys",
            },
        ),
        migrations.CreateModel(
            name="ProcessedListings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("query", models.CharField(default="", max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("link", models.URLField()),
                ("listing_type", models.CharField(max_length=100)),
                ("bedroom", models.FloatField()),
                ("bathrooms", models.FloatField()),
                ("location", models.CharField(max_length=255)),
                ("town", models.CharField(max_length=255)),
                ("price", models.FloatField()),
                ("pricepermonth", models.CharField(max_length=500)),
                ("views", models.IntegerField()),
                ("reactions", models.IntegerField()),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="listings.listing",
                    ),
                ),
            ],
            options={
                "db_table": "processed_listing",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.URLField()),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listing_image",
                        to="listings.listing",
                    ),
                ),
            ],
            options={
                "db_table": "listing_images",
            },
        ),
    ]
