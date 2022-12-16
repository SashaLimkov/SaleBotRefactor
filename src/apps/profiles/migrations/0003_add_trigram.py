import datetime
from django.db import migrations, models
from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        TrigramExtension(),
        UnaccentExtension()
    ]
