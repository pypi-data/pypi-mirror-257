def to_camel_case(text):
    if not text:
        return text
    return "".join(x for x in text.title() if not x.isspace())
