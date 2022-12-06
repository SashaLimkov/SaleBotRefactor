from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from django.utils import timezone

from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = "Start Periodic Task"

    def handle(self, *args, **options):
        interval = IntervalSchedule.objects.get_or_create(every=24, period=IntervalSchedule.HOURS)

        try:
            PeriodicTask.objects.create(
                name='Repeat Update Metric',
                task='repeat_update_metric',
                interval=interval[0],
                start_time=timezone.now()
            )

            PeriodicTask.objects.create(
                name='Repeat Update Subscription',
                task='repeat_update_subscriptions',
                interval=interval[0],
                start_time=timezone.now()
            )
            print('Start periodic tasks - COMPLETE')
        except ValidationError:
            print('Start periodic tasks - ERROR [A periodic task with the same name already exists]')
