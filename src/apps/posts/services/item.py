from apps.posts.models import Item


def create_item(post_id: int, name: str, link: str, sizes: str,
                description: str, price_old: float, price_new: float) -> Item:
    """Создает позицию товара привязанную к посту"""
    return Item.objects.create(
        post_id=post_id,
        name=name,
        link=link,
        sizes=sizes,
        description=description,
        price_old=price_old,
        price_new=price_new
    )


def update_item(item_id: int, name: str, link: str, sizes: str,
                description: str, price_old: float, price_new: float) -> Item:
    item = Item.objects.get(pk=item_id)
    item.name = name
    item.link = link
    item.sizes = sizes
    item.description = description
    item.price_old = price_old
    item.price_new = price_new
    item.save()
    return item
