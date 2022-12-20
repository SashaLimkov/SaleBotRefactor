from typing import Union, List, Tuple

from django.db.models import QuerySet

from apps.posts.models import Post, UserPost
from apps.posts.services.content import watermark
from apps.posts.services.shop import get_or_create_shop
from apps.settings.services.course import get_value_course_user_by_currency
from apps.settings.services.currency import get_course_currency
from apps.settings.services.settings_user import get_settings
from bot.utils.rounder import round_num_to


def get_posts_by_compilation_id(compilation_id: int) -> Union[QuerySet, List[Post]]:
    """Возвращает QuerySet постов по id подборки"""
    return (
        Post.objects.filter(compilation_id=compilation_id)
            .select_related("compilation", "shop")
            .prefetch_related("items", "contents", "user_post", "shop__currency")
    )


def get_formatted_channel_posts_by_compilation_id(compilation_id: int) -> list:
    """Возвращает список с сформированным текстом для постов"""
    posts = get_posts_by_compilation_id(compilation_id)
    result = []
    for index, post in enumerate(posts):
        contents = None
        post_text = post.shop.name + "\n\n"
        for item in post.items.all():
            post_text += item.name + "\n" if item.name else ''
            post_text += item.sizes + "\n" if item.sizes else ''
            post_text += item.description + "\n" if item.description else ''
            post_text += (
                f"Цена: <b><s>{item.price_old}{post.shop.currency.sign}</s>➡️"
            )
            post_text += f"{item.price_new}{post.shop.currency.sign}</b>" + "\n"
            post_text += f'{item.link}\n'
        for content in post.contents.all():

            contents = [(content.type, content.file.path)]
        result.append((post_text, contents, post))

    return result


def get_formatted_posts_by_compilation_id(
        compilation_id: int,
) -> list:
    """Возвращает список с дополнительными полями (сформированный текст и контент)"""
    posts = get_posts_by_compilation_id(compilation_id)
    result = []
    for index, post in enumerate(posts):
        contents = None
        post_text = post.shop.name + "<br><br>"
        for item in post.items.all():
            post_text += item.name + "<br>" if item.name else ''
            post_text += item.sizes + "<br>" if item.sizes else ''
            post_text += item.description + "<br>" if item.description else ''
            price_old = item.price_old
            price_new = item.price_new
            post_text += f"Цена: <b><s>{price_old}{post.shop.currency}</s>"
            if price_new:
                post_text += f"➡️{price_new}{post.shop.currency}</b>" + "\n"
            post_text += f"{item.price_new}{post.shop.currency.sign}</b>" + "<br>"
            post_text += f'<a href="{item.link}">{item.link}</a><br>'
        for content in post.contents.all():
            contents = {'url': content.file.url, 'type': content.type}
        result.append({'text': post_text, 'content': contents, 'pk': post.pk, 'obj': post, 'id': index + 1})
    return result


def get_formatted_user_settings_posts_by_compilation_id(
        compilation_id: int, telegram_id: int, channel=0
) -> List[Tuple[str, List[Tuple[str, str]]]]:
    """Возвращает посты на основе настроек пользователя в формате Tuple['текст поста', Tuple['список медиа']]
    Аргумент channel, принимает значение 0 - отправка в TG и 1 - отправка в ВК"""
    posts = get_posts_by_compilation_id(compilation_id)
    settings = get_settings(telegram_id)
    result_user_list = []
    for post in posts:
        contents = []
        if not post.user_post.filter(profile_id=telegram_id):
            post_text = post.compilation.name + "\n\n"
            for item in post.items.all():
                if settings.product_settings.name:
                    if settings.hided_link and channel == 0:
                        post_text += f'<a href="{item.link}">{item.name}</a>\n'
                    else:
                        post_text += item.name + "\n"
                if settings.product_settings.sizes:
                    post_text += item.sizes + "\n" if item.sizes else ''
                if settings.product_settings.description:
                    post_text += item.description + "\n" if item.description else ''
                if settings.product_settings.price:
                    if settings.currency == 0:
                        price_old = item.price_old
                        price_new = item.price_new
                        sign = post.shop.currency.sign
                    else:
                        user_course = get_value_course_user_by_currency(
                            post.shop.currency.currency, telegram_id
                        )
                        if user_course:
                            price_old = item.price_old * user_course.value
                            price_new = item.price_new * user_course.value
                        else:
                            course = get_course_currency(post.shop.currency.currency)
                            price_old = item.price_old * course
                            price_new = item.price_new * course
                        sign = "₽"
                    if settings.formula:
                        price_old = price_old + (price_old / 100 * settings.commission)
                        price_new = price_new + (price_new / 100 * settings.commission)
                    if settings.rounder:
                        price_old = round_num_to(price_old, settings.rounder, settings.currency)
                        price_new = round_num_to(price_new, settings.rounder, settings.currency)
                    post_text += f"<b><s>{price_old}{sign}</s>"
                    if price_new:
                        post_text += f"➡️{price_new}{sign}</b>" + "\n"
                if settings.product_settings.link:
                    if settings.link and channel == 0 and not settings.hided_link:
                        post_text += f'<a href="{item.link}">Ссылка</a>'
                    else:
                        post_text += item.link
                if settings.signature:
                    post_text += "\n\n" + settings.signature
            for content in post.contents.all():
                if (settings.logo or settings.text_logo) and content.type == 0:
                    contents.append((0, watermark(content.file.path, settings.logo,
                                                  settings.logo_position, settings.text_logo)))
                else:
                    contents.append((content.type, content.file.path))
        else:
            for content in post.contents.all():
                if (settings.logo or settings.text_logo) and content.type == 0:
                    contents.append((0, watermark(content.file.path, settings.logo,
                                                  settings.logo_position, settings.text_logo)))
                else:
                    contents.append((content.type, content.file.path))
            post_text = post.user_post.all()[0].text
        result_user_list.append((post_text, contents, post.pk))
    # result_user_list.reverse()
    return result_user_list


def add_user_post(post_id: int, text: str, telegram_id: int) -> UserPost:
    """Добавляет пользовательский пост, наследованный от оригинального поста"""
    return (
        UserPost.objects.select_related("post", "profile")
            .prefetch_related("post__compilation", "post__shop")
            .update_or_create(
            post_id=post_id, profile_id=telegram_id, defaults={"text": text}
        )
    )


def get_user_post(post_id: int, telegram_id: int) -> UserPost:
    """Возвращает пользовательский пост"""
    return UserPost.objects.filter(post_id=post_id, telegram_id=telegram_id).first()


def delete_user_post(post_id: int, telegram_id: int) -> None:
    """Удаляет пользовательский пост"""
    UserPost.objects.get(post_id=post_id, profile_id=telegram_id).delete()


def create_post(compilation_id: int, shop: str, currency_id: int):
    """Создает пост привязанный к подборке"""
    return Post.objects.create(
        compilation_id=compilation_id,
        shop=get_or_create_shop(shop, currency_id)
    )


def update_post(post_id: int, shop: str, currency_id: int):
    """Обновляет пост привязанный к подборке"""
    shop = get_or_create_shop(shop, currency_id)
    post = Post.objects.get(pk=post_id)
    post.shop = shop
    post.save()
    return post
