from apps.posts.models import Shop


def get_or_create_shop(name: str, currency_id: int) -> Shop:
    """Возвращает или создает новый магазин"""
    shop = Shop.objects.filter(name=name, currency_id=currency_id).first()
    if not shop:
        shop = Shop.objects.create(name=name, currency_id=currency_id)
    return shop
