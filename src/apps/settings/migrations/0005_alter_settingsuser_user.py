# Generated by Django 4.1.3 on 2022-12-10 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0016_alter_profile_last_action_date_and_more"),
        ("settings", "0004_remove_productsettings_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="settingsuser",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="profiles.profile",
                verbose_name="Пользователь",
            ),
        ),
    ]