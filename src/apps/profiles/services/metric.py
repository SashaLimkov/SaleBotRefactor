from apps.profiles.models import Profile, ProfileMetric
from apps.utils.services.date_time import get_date_now


def update_metrics_profiles_for_past_day() -> None:
    """Сохранения количества действий пользователей за текущий день в таблицу ProfileMetric"""
    date = get_date_now()
    profiles = Profile.objects.all().only('count_actions_in_current_day')
    profiles_metric = []
    for profile in profiles:
        profiles_metric.append(ProfileMetric(profile=profile, date=date,
                                             count_actions=profile.count_actions_in_current_day))
    profiles.update(count_actions_in_current_day=0)
    ProfileMetric.objects.abulk_create(profiles_metric)
