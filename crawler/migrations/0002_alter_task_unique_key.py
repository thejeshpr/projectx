# Generated by Django 4.1.1 on 2023-03-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crawler", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="unique_key",
            field=models.CharField(max_length=2500, unique=True),
        ),
    ]
