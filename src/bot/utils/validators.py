async def is_float_number(s: str) -> bool:
    try:
        s = s.replace(",", ".")
        float(s)
        return True
    except ValueError:
        return False
