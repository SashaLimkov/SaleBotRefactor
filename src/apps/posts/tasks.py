import time

from celery import shared_task

from bot.handlers.main.posts.posts import send_final_compilation
from bot.utils.message_worker import try_send_post_to_user
from .models import Compilation, Post
from django.utils import timezone

from .services.compilation import get_final_compilation
from .services.post import get_formatted_channel_posts_by_compilation_id

from django.conf import settings

import asyncio


@shared_task(name='send_post')
def time_send_post():
    for compilation in Compilation.objects.filter(datetime_send__lte=timezone.now(), message_id=None).prefetch_related('contents'):
        posts = get_formatted_channel_posts_by_compilation_id(compilation.id)

        content = compilation.contents.first()
        compilation.message_id = asyncio.run(try_send_post_to_user(content.file.path, content.type, settings.CHANNEL, compilation.text))
        compilation.save()
        for post in posts:
            post[2].message_id = asyncio.run(try_send_post_to_user(post[1][0][1], post[1][0][0], settings.CHANNEL, post[0]))
            post[2].save()

            time.sleep(1)

        final = get_final_compilation(compilation_id=compilation.id)
        if final:
            content = final.contents.first()
            final.message_id = asyncio.run(try_send_post_to_user(content.file.path, content.type, settings.CHANNEL, final.text))
            final.save()
