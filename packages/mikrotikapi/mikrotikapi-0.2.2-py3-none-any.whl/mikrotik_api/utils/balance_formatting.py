import locale


def sum_formatting(value: str | float | int):
    if isinstance(value, str):
        value = float(value)

    # Преобразование числа в целое
    value = int(value)

    # Форматирование целой части числа с пробелами
    formatted_value = "{:,}".format(value).replace(",", " ")

    return formatted_value
