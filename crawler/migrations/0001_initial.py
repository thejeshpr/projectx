# Generated by Django 4.1.1 on 2023-03-08 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="ConfigValues",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "key",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                ("val", models.CharField(blank=True, max_length=250, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Job",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("error", models.TextField(blank=True, null=True)),
                ("elapsed_time", models.IntegerField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "NEW"),
                            ("RUNNING", "RUNNING"),
                            ("SUCCESS", "SUCCESS"),
                            ("ERROR", "ERROR"),
                            ("NO-TASK", "NO-TASK"),
                        ],
                        default="NEW",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SiteConf",
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
                ("base_url", models.CharField(blank=True, max_length=250, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("enabled", models.BooleanField(default=True)),
                (
                    "extra_data_json",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        default="las la-question-circle",
                        max_length=50,
                        null=True,
                    ),
                ),
                ("is_locked", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "scraper_name",
                    models.CharField(blank=True, max_length=25, null=True),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="site_confs",
                        to="crawler.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("data", models.TextField(blank=True, null=True)),
                ("is_bookmarked", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=500)),
                ("unique_key", models.CharField(max_length=250, unique=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("url", models.URLField(blank=True, null=True)),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="crawler.job",
                    ),
                ),
                (
                    "site_conf",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="crawler.siteconf",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="job",
            name="site_conf",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="jobs",
                to="crawler.siteconf",
            ),
        ),
        migrations.CreateModel(
            name="ExtraTaskData",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("data", models.CharField(blank=True, max_length=2000, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="extra_data",
                        to="crawler.task",
                    ),
                ),
            ],
        ),
    ]
