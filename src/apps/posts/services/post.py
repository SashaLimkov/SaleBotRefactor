from typing import Union, List, Tuple

from django.db.models import QuerySet

from apps.posts.models import Post, UserPost


def get_posts_by_compilation_id(compilation_id: int) -> Union[QuerySet, List[Post]]:
    """Возвращает QuerySet постов по id подборки"""
    return Post.objects.filter(compilation_id=compilation_id)\
        .select_related('compilation', 'shop')\
        .prefetch_related('items', 'contents', 'user_post', 'shop__currency')


def get_formatted_posts_by_compilation_id(compilation_id: int) -> List[Tuple[str, List[Tuple[str, str]]]]:
    """Возвращает кортеж форматированных постов в формате Tuple['текст поста', Tuple['список медиа']]"""
    posts = get_posts_by_compilation_id(compilation_id)
    result_list = []
    for post in posts:
        contents = []
        if not post.user_post.all():
            post_text = post.compilation.name + '\n\n'
            for item in post.items.all():
                post_text += item.name + '\n'
                post_text += item.sizes + '\n'
                post_text += item.description + '\n'
                post_text += f'Цена: <b><s>{item.price_old}{post.shop.currency.sign}</s>➡️'
                post_text += f'{item.price_new}{post.shop.currency.sign}</b>' + '\n'
                post_text += item.link
            for content in post.contents.all():
                contents.append((content.type, content.file.path))
        else:
            post_text = post.user_post.all()[0].text
        result_list.append((post_text, contents))
    return result_list


def add_user_post(post_id: int, text: str, telegram_id: int) -> UserPost:
    """Добавляет пользовательский пост, наследованный от оригинального поста"""
    return UserPost.objects.select_related('post', 'profile').prefetch_related('post__compilation', 'post__shop')\
                                                             .update_or_create(post_id=post_id,
                                                                               profile_id=telegram_id,
                                                                               defaults={"text": text})


def delete_user_post(post_id: int, telegram_id: int) -> None:
    """Удаляет пользовательский пост"""
    UserPost.objects.get(post_id=post_id, profile_id=telegram_id).delete()
