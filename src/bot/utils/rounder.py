def round_num_to(num, round_lvl: int, currency: int) -> str:
    if not currency:
        r = f'{float("{:.2f}".format(num))}'
        return r if len(r.split(".")[-1]) == 2 else r + "0"
    if round_lvl == 0:
        return str(round(float(num),2))
    if round_lvl == 1:
        return f"{int(num) if int(str(int(num))) == float(num) else int(num) + 1}"
    elif round_lvl == 2:
        number = (
            (int(num) // 10 + 1) * 10 if int(num) / 10 != int(num) // 10 else int(num)
        )
        r = f'{float("{:.2f}".format(number))}'
        return str(int(r[:-2]))
    elif round_lvl == 3:
        number = (
            50 * (int(num) // 50 + 1) if int(num) / 50 != int(num) // 50 else int(num)
        )
        r = f'{float("{:.2f}".format(number))}'
        return str(int(r[:-2]))
    else:
        number = (
            100 * (int(num) // 100 + 1)
            if int(num) / 100 != int(num) // 100
            else int(num)
        )
        r = f'{float("{:.2f}".format(number))}'
        return str(int(r[:-2]))
