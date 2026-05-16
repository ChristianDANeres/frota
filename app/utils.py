import re


def format_cpf(value):
    if not value:
        return ''
    s = re.sub(r"\D", "", str(value))
    if len(s) == 11:
        return f"{s[0:3]}.{s[3:6]}.{s[6:9]}-{s[9:11]}"
    return value
