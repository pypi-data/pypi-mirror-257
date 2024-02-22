import pymorphy3


def pluralize_word(word, number):
    morph = pymorphy3.MorphAnalyzer()
    parsed = morph.parse(word)[0]

    # Получение формы слова во множественном числе
    plural_form = parsed.make_agree_with_number(number).word

    return plural_form
