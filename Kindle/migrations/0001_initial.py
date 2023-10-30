# Generated by Django 4.2.6 on 2023-10-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("color", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Highlight",
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
                ("book_title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=200)),
                ("highlight_text", models.TextField()),
                ("location", models.IntegerField()),
                ("tags", models.ManyToManyField(to="Kindle.tag")),
            ],
        ),
    ]
