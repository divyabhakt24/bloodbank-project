# Generated by Django 4.2.20 on 2025-05-02 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bloodbankapp", "0002_alter_bloodrequest_required_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodrequest",
            name="required_by",
            field=models.DateField(
                default=datetime.datetime(
                    2025, 5, 5, 9, 21, 7, 497501, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
