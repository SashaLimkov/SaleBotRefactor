from apps.profiles.models import Profile


def get_count_user() -> int:
    return Profile.objects.count()


def get_count_user_unsub() -> int:
    return

