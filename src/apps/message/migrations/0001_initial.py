# Generated by Django 4.1.4 on 2022-12-16 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
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
                        max_length=60, unique=True, verbose_name="Название"
                    ),
                ),
                ("text", models.TextField(blank=True, null=True, verbose_name="Текст")),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.CreateModel(
            name="Keyboard",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "type",
                    models.IntegerField(
                        choices=[(0, "Reply"), (1, "Inline")], verbose_name="Тип"
                    ),
                ),
                (
                    "one_time_keyboard",
                    models.BooleanField(
                        default=False, verbose_name="Одноразовая клавиатура"
                    ),
                ),
                (
                    "row_width",
                    models.IntegerField(verbose_name="Количество кнопок в ряду"),
                ),
                (
                    "message",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="message.message",
                        verbose_name="Сообщение",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MessageContent",
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
                ("file", models.FileField(upload_to="", verbose_name="Файл")),
                (
                    "message",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="message.message",
                        verbose_name="Сообщение",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Button",
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
                    "text",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Текст"
                    ),
                ),
                (
                    "url",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="URL"
                    ),
                ),
                (
                    "callback_data",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Callback Data",
                    ),
                ),
                (
                    "keyboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="message.keyboard",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
