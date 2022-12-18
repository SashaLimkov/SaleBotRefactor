from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.data import callback_data as cd
from bot.handlers.main.posts import date_and_inline, posts, post_senders
from bot.states.Posts import PostStates


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        date_and_inline.show_compilations_by_date_call,
        cd.select_date.filter(),
        state="*"
    )
    dp.register_inline_handler(
        date_and_inline.inline_compilations,
        state="*"
    )
    dp.register_message_handler(
        posts.sender_anons,
        filters.Text(contains="|:|"),
        state="*"
    )
    dp.register_callback_query_handler(
        posts.edit_is_send_post,
        cd.turn_on_or_off_post.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        posts.select_platform,
        cd.send_one_or_all.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        posts.get_post_or_compilation,
        cd.get_post_by_id.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        posts.select_channel,
        cd.select_platform.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        post_senders.send_posts,
        cd.select_channel.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        posts.change_post,
        cd.change_post.filter(),
        state="*",
    )
    dp.register_message_handler(
        posts.keep_updated_post,
        state=PostStates.GET_TEXT
    )
