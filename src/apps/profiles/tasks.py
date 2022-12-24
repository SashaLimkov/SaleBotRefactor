from celery import shared_task

from .services.subscription import decrement_number_of_days_left
from .services.metric import update_metrics_profiles_for_past_day


@shared_task(name="repeat_update_metric")
def repeat_update_metric():
    """Периодичная задача обновления метрик"""
    update_metrics_profiles_for_past_day()


@shared_task(name="repeat_update_subscriptions")
def repeat_update_subscriptions():
    """Периодичная задача обновления подписок пользователей"""
    decrement_number_of_days_left()
    # turn_on_sub_with_days()
