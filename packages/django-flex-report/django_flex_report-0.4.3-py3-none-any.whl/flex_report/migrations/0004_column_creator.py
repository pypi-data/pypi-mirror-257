# Generated by Django 4.2.7 on 2023-11-22 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("flex_report", "0003_column_groups_column_users_tablebutton_groups_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="column",
            name="creator",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_columns",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
