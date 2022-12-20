import datetime
from typing import Any

from django.contrib.auth.models import User

from apps.users.models import Log


def create_log(user: User, type_log: int, to: Any = None) -> Log:
    date = datetime.datetime.now()
    if type_log < 3 and to:
        return Log.objects.create(user=user, datetime=date, type=type_log, post=to)
    elif 2 < type_log < 6 and to:
        return Log.objects.create(user=user, datetime=date, type=type_log, compilation=to)
    elif 5 < type_log < 9 and to:
        return Log.objects.create(user=user, datetime=date, type=type_log, final_compilation=to)
