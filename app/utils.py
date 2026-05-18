import re


def format_cpf(value):
    if not value:
        return ''
    s = re.sub(r"\D", "", str(value))
    if len(s) == 11:
        return f"{s[0:3]}.{s[3:6]}.{s[6:9]}-{s[9:11]}"
    return value


def format_money(value):
    if value is None:
        return '-'
    try:
        v = float(value)
    except Exception:
        return str(value)
    # formata com separador de milhares '.' e decimal ',' para Brasil
    s = "{:,.2f}".format(v)
    # s usa ',' como thousands sep e '.' como decimal in default locale (en)
    # invertendo para PT-BR: '.' milhares, ',' decimal
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f"R$ {s}"
