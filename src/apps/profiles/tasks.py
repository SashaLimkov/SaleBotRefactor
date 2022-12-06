from celery import shared_task

from .services.subscription import decrement_number_of_days_left
from .services.metric import update_metrics_profiles_for_past_day


@shared_task(name="repeat_update_metric")
def repeat_update_metric():
    decrement_number_of_days_left()


@shared_task(name="repeat_update_subscriptions")
def repeat_update_subscriptions():
    update_metrics_profiles_for_past_day()
