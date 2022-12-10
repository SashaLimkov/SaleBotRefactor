from apps.profiles.models import Profile, ProfileMetric
from apps.utils.services.date_time import get_date_now


def update_metrics_profiles_for_past_day() -> None:
    """Сохранения количества действий пользователей за текущий день в таблицу ProfileMetric"""
    date = get_date_now()
    profiles = Profile.objects.all().only('count_actions_in_current_day', 'telegram_id', 'count_days_in_bot',
                                          'count_actions', 'activity')
    profiles_metric = []
    profiles_update_activity = []
    for profile in profiles:
        profiles_metric.append(ProfileMetric(profile_id=profile.telegram_id, date=date,
                                             count_actions=profile.count_actions_in_current_day))
        profile.count_days_in_bot += 1
        profile.count_actions += profile.count_actions_in_current_day
        profile.activity = profile.count_actions / profile.count_days_in_bot
        profiles_update_activity.append(profile)
    profiles.update(count_actions_in_current_day=0)
    profiles.bulk_update(profiles_update_activity, ['count_days_in_bot', 'count_actions', 'activity'])
    ProfileMetric.objects.bulk_create(profiles_metric)
