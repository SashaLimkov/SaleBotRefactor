# Generated by Django 4.1.4 on 2022-12-17 06:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активный"),
                ),
                (
                    "is_helper",
                    models.BooleanField(default=False, verbose_name="Помощник"),
                ),
                (
                    "is_blocked",
                    models.BooleanField(default=False, verbose_name="Забанен"),
                ),
                ("in_chat", models.BooleanField(default=False, verbose_name="В чате")),
                (
                    "telegram_id",
                    models.BigIntegerField(
                        db_index=True, unique=True, verbose_name="ID Telegram"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Username Telegram",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Имя в Telegram",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Фамилия в Telegram",
                    ),
                ),
                (
                    "phone",
                    models.CharField(max_length=15, verbose_name="Номер телефона"),
                ),
                ("full_name", models.CharField(max_length=255, verbose_name="ФИО")),
                (
                    "registration_date",
                    models.DateTimeField(
                        default=datetime.datetime(2022, 12, 17, 9, 46, 56, 689391),
                        verbose_name="Дата регистрации",
                    ),
                ),
                (
                    "last_action_date",
                    models.DateTimeField(
                        default=datetime.datetime(2022, 12, 17, 9, 46, 56, 689391),
                        verbose_name="Дата последней активности",
                    ),
                ),
                ("activity", models.FloatField(default=0.0, verbose_name="Активность")),
                (
                    "count_actions_in_current_day",
                    models.IntegerField(
                        default=0, verbose_name="Количество действий за текущий день"
                    ),
                ),
                (
                    "count_days_in_bot",
                    models.IntegerField(
                        default=0, verbose_name="Количество дней в боте"
                    ),
                ),
                (
                    "count_actions",
                    models.IntegerField(
                        default=0, verbose_name="Общее количество действий"
                    ),
                ),
                (
                    "inviting_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                        to_field="telegram_id",
                        verbose_name="Пригласивший пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь Telegram",
                "verbose_name_plural": "Пользователи Telegram",
            },
        ),
        migrations.CreateModel(
            name="Rate",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "displayed",
                    models.BooleanField(default=True, verbose_name="Отображается"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("price", models.FloatField(verbose_name="Цена")),
                (
                    "currency",
                    models.CharField(max_length=5, verbose_name="Идентификатор валюты"),
                ),
                (
                    "count_day_sub",
                    models.IntegerField(verbose_name="Количество дней подписки"),
                ),
            ],
            options={
                "verbose_name": "Тариф",
                "verbose_name_plural": "Тарифы",
            },
        ),
        migrations.CreateModel(
            name="Subscription",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True, verbose_name="Активна")),
                (
                    "datetime_buy",
                    models.DateTimeField(
                        default=datetime.datetime(2022, 12, 17, 9, 46, 56, 705013),
                        verbose_name="Время покупки",
                    ),
                ),
                (
                    "datetime_end",
                    models.DateTimeField(verbose_name="Время окончания подиски"),
                ),
                (
                    "cheque",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Чек"
                    ),
                ),
                ("days_left", models.IntegerField(verbose_name="Осталось дней")),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                        to_field="telegram_id",
                        verbose_name="Пользователь",
                    ),
                ),
                (
                    "rate",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="profiles.rate",
                        verbose_name="Тариф",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
        migrations.CreateModel(
            name="ProfileMetric",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateField()),
                ("count_actions", models.IntegerField()),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                        to_field="telegram_id",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
