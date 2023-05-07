import re

from unidecode import unidecode


def slug(text: str):
    result = text.lower()
    result = unidecode(result)
    result = result.replace(" ", "")
    return re.sub("[^a-zA-Z0-9]", "", result)
