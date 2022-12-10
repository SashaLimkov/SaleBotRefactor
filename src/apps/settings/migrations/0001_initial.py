# Generated by Django 4.1.3 on 2022-12-06 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("profiles", "0004_alter_profile_last_action_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Currency",
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
                    "name",
                    models.CharField(
                        max_length=20, verbose_name="Название валюты (в боте)"
                    ),
                ),
                ("currency", models.CharField(max_length=4, verbose_name="Валюта")),
                (
                    "sign",
                    models.CharField(
                        blank=True, max_length=1, null=True, verbose_name="Знак валюты"
                    ),
                ),
            ],
            options={
                "verbose_name": "Валюта",
                "verbose_name_plural": "Валюты",
            },
        ),
        migrations.CreateModel(
            name="ProductSettings",
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
                ("link", models.BooleanField(default=True, verbose_name="Ссылка")),
                ("name", models.BooleanField(default=True, verbose_name="Название")),
                ("price", models.BooleanField(default=True, verbose_name="Цена")),
                ("discount", models.BooleanField(default=True, verbose_name="Скидка")),
                ("sizes", models.BooleanField(default=True, verbose_name="Размеры")),
                (
                    "description",
                    models.BooleanField(default=True, verbose_name="Описание"),
                ),
            ],
            options={
                "verbose_name": "Настройку товара",
                "verbose_name_plural": "Настройки товара",
            },
        ),
        migrations.CreateModel(
            name="SettingsUser",
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
                    "formula",
                    models.IntegerField(
                        choices=[(0, "Без комиссии"), (1, "С комиссией")],
                        default=0,
                        verbose_name="Формула ценообразования",
                    ),
                ),
                (
                    "commission",
                    models.FloatField(
                        blank=True, default=0.0, null=True, verbose_name="Комиссия"
                    ),
                ),
                (
                    "rounder",
                    models.IntegerField(
                        blank=True,
                        default=1,
                        null=True,
                        verbose_name="Уровень округления",
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="Логотип"
                    ),
                ),
                (
                    "text_logo",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Текстовый Логотип",
                    ),
                ),
                (
                    "logo_position",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Позиция лого",
                    ),
                ),
                ("signature", models.TextField(default="", verbose_name="Подпись")),
                (
                    "link",
                    models.BooleanField(default=False, verbose_name="Короткая ссылка"),
                ),
                (
                    "hided_link",
                    models.BooleanField(default=False, verbose_name="Ссылка в тексте"),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="settings.currency",
                        verbose_name="Валюта",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="settings.productsettings",
                        verbose_name="Настройки продукт",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Общую настройку",
                "verbose_name_plural": "Общие настройки пользователей",
            },
        ),
        migrations.CreateModel(
            name="ChanelVk",
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
                ("chat_id", models.BigIntegerField(verbose_name="ID Канала")),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Канал в ВК",
                "verbose_name_plural": "Каналы в ВК",
            },
        ),
        migrations.CreateModel(
            name="ChanelTelegram",
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
                ("chat_id", models.BigIntegerField(verbose_name="ID Канала")),
                (
                    "name_channel",
                    models.CharField(max_length=255, verbose_name="Название канала"),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Канал в Telegram",
                "verbose_name_plural": "Каналы в Telegram",
            },
        ),
    ]