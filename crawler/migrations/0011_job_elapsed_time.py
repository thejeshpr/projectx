# Generated by Django 4.1.1 on 2022-09-25 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0010_alter_job_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='elapsed_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
