from django.core.management import BaseCommand
from apps.profiles.services.profile import create_user


class Command(BaseCommand):
    help = "Start Periodic Task"

    def handle(self, *args, **options):
        for i in range(300, 50000):
            create_user(
                telegram_id=i,
                phone='123243534',
                full_name='Assdg hdfghrh'
            )
