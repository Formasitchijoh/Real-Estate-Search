# Generated by Django 5.0.6 on 2024-06-17 11:08

from django.db import migrations, models


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
                ("title", models.CharField(max_length=1000)),
                ("image", models.CharField(max_length=500)),
                ("link", models.CharField(max_length=200)),
                ("listing_type", models.CharField(max_length=50)),
                ("bedroom", models.CharField(max_length=200)),
                ("bathrooms", models.CharField(max_length=200)),
                ("location", models.CharField(max_length=50)),
                ("town", models.CharField(max_length=50)),
                ("price", models.CharField(max_length=200)),
                ("pricepermonth", models.CharField(max_length=50)),
                ("views", models.CharField(max_length=200)),
                ("reactions", models.IntegerField()),
            ],
        ),
    ]
