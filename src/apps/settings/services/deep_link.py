from apps.settings.models.deep_link import DeepLink


def create_deep_link(telegram_id: int, deep_link: str, identifier: int):
    dl = DeepLink(
        creator_id=telegram_id,
        deep_link=deep_link,
        identifier=identifier,
        used=False
    )
    dl.save()
    return dl


def get_deep_link_by_identifier_and_tg_id(identifier: int, tg_id:int):
    return DeepLink.objects.filter(identifier=identifier, creator_id=tg_id).first()


def close_deep_link_identifier_and_tg_id(identifier: int, tg_id:int):
    dl = DeepLink.objects.filter(identifier=identifier, creator_id=tg_id).first()
    dl.used = True
    dl.save()
