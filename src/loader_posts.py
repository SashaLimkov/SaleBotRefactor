import datetime
import os, django
import pickle


def load():
    from bot_backend.models import Compilation

    list_compilations = []

    for compilation in Compilation.objects.filter(date__gt=datetime.date.today() - datetime.timedelta(days=3)):
        compilation_dict = {
            'message_id': compilation.message_id,
            'date': compilation.date,
            'name': compilation.name,
            'done': compilation.done,
            'text': compilation.text_obzor,
            'datetime_send': compilation.date,
            'content': (0, compilation.photo_obzor.path) if compilation.photo_obzor else (1, compilation.video_obzor.path),
            'gid':
                {
                    'message_id': compilation.gid.message_id,
                    'text': compilation.gid.text_gid,
                    'content': (0, compilation.gid.photo_gid.path) if compilation.gid.photo_gid else (
                                1, compilation.gid.video_gid.path),
                } if hasattr(compilation, 'gid') else None,
            'posts': [
                {
                    'shop':
                        {
                            'name': post.shop.name,
                            'currency': post.shop.currency.name
                        },
                    'message_id': post.message_id,
                    'content': (0, post.photo.path) if post.photo else (
                                1, post.video.path),
                    'items': [
                        {
                            'name': item.name,
                            'link': item.link,
                            'sizes': item.sizes,
                            'description': item.description,
                            'price_old': item.discount,
                            'price_new': item.cost
                        }
                        for item in post.items.all()
                    ]
                }
                for post in compilation.post_set.all()
            ]
        }
        list_compilations.append(compilation_dict)
    with open('data.pickle', 'wb') as file:
        pickle.dump(list_compilations, file)



if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegrambot.settings")
    django.setup()
    load()
