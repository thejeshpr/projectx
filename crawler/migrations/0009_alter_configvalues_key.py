# Generated by Django 4.1.1 on 2022-09-24 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0008_configvalues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configvalues',
            name='key',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
