import pickle, os, django


def load():
    from apps.posts.models import Compilation, Content, Post, Item, Shop, FinalCompilation
    from apps.settings.models import Currency
    with open('data.pickle', 'rb') as file:
       data = pickle.load(file)

    for compilation_dict in data:
        compilation = Compilation(
            date=compilation_dict['date'],
            name=compilation_dict['name'],
            done=compilation_dict['done'],
            text=compilation_dict['text'],
            message_id=compilation_dict['message_id'],
            datetime_send=compilation_dict['datetime_send']
        )
        compilation.save()
        content_comp = Content(
            compilation=compilation,
            type=compilation_dict['content'][0]
        )
        file_name = compilation_dict['content'][1].split('/')[-1]
        with open(f'old_data/{file_name}', 'rb') as file:
            content_comp.file.save(file_name, file)
        content_comp.save()
        for post_dict in compilation_dict['posts']:
            currency = Currency.objects.get(name=post_dict['shop']['currency'])
            shop = Shop.objects.filter(name=post_dict['shop']['name'], currency=currency).first()
            if shop is None:
                shop = Shop(
                    name=post_dict['shop']['name'],
                    currency=currency
                )
                shop.save()
            post = Post(
                compilation=compilation,
                shop=shop,
                message_id=post_dict['message_id']
            )
            post.save()

            content_post = Content(
                post=post,
                type=post_dict['content'][0]
            )
            file_name = post_dict['content'][1].split('/')[-1]
            with open(f'old_data/{file_name}', 'rb') as file:
                content_post.file.save(file_name, file)
            content_post.save()

            for item in post_dict['items']:
                try:
                    Item.objects.create(
                        post=post,
                        name=item['name'],
                        link=item['link'],
                        sizes=item['sizes'],
                        description=item['description'],
                        price_old=item['price_old'],
                        price_new=item['price_new']
                    )
                except:
                    pass
        if compilation_dict['gid']:
            gid = FinalCompilation(
                compilation=compilation,
                text=compilation_dict['gid']['text'],
                message_id=compilation_dict['gid']['message_id'],
            )
            gid.save()

            content_gid = Content(
                final_compilation=gid,
                type=compilation_dict['gid']['content'][0]
            )
            file_name = compilation_dict['gid']['content'][1].split('/')[-1]
            with open(f'old_data/{file_name}', 'rb') as file:
                content_gid.file.save(file_name, file)
            content_gid.save()


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()
    load()
