from datetime import datetime, timedelta


async def get_datetime(key):
    day = datetime.today()
    today = datetime(day.year, day.month, day.day)
    if key == "td":
        return datetime(today.year, today.month, today.day)
    elif key == "yt":
        yesterday = today - timedelta(days=1)
        return datetime(yesterday.year, yesterday.month, yesterday.day)
    elif key == "2t":
        yesterday = today - timedelta(days=2)
        return datetime(yesterday.year, yesterday.month, yesterday.day)
    elif key == "3t":
        yesterday = today - timedelta(days=3)
        return datetime(yesterday.year, yesterday.month, yesterday.day)
    else:
        tomorrow = today + timedelta(days=1)
        return datetime(tomorrow.year, tomorrow.month, tomorrow.day)
