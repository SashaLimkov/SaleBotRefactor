# Generated by Django 4.1.4 on 2022-12-18 12:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="last_action_date",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 12, 18, 15, 23, 57, 172860),
                verbose_name="Дата последней активности",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="registration_date",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 12, 18, 15, 23, 57, 172842),
                verbose_name="Дата регистрации",
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="datetime_buy",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 12, 18, 15, 23, 57, 174678),
                verbose_name="Время покупки",
            ),
        ),
    ]
