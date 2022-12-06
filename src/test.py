import django, os


def run():
    from apps.profiles.services.profile import create_profile


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()
    run()
