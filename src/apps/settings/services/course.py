from apps.settings.models import CourseUser


def get_value_course_user_by_currency(
    currency_name: str, telegram_id: int
) -> CourseUser:
    """Возвращает курса пользователя по названию валюты"""
    return CourseUser.objects.filter(
        currency_id=currency_name, profile_id=telegram_id
    ).first()


def get_all_course_user(telegram_id: int) -> list[CourseUser]:
    return (
        CourseUser.objects.filter(profile_id=telegram_id)
        .all()
        .select_related("currency")
    )


def add_or_update_course_user(
    currency_name: str, telegram_id: int, value: float
) -> CourseUser:
    """Создает или обновляет курс пользователя"""
    return CourseUser.objects.get_or_create(
        currency_id=currency_name, profile_id=telegram_id, defaults={"value": value}
    )
