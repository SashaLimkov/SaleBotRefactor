from apps.posts.models import Shop


def get_or_create_shop(name: str, currency_id: int) -> Shop:
    """Возвращает или создает новый магазин"""
    return Shop.objects.get_or_create(name=name, defaults={'currency_id': currency_id})[0]
