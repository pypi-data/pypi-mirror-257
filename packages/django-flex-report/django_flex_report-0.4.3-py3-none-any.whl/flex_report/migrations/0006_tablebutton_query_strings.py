# Generated by Django 5.0.1 on 2024-01-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flex_report", "0005_template_model_user_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="tablebutton",
            name="query_strings",
            field=models.JSONField(
                blank=True, default=dict, verbose_name="Query String"
            ),
        ),
    ]
