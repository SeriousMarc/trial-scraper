import re

def string_to_number(_str):
    _str = ''.join(re.findall(r'\d+', _str))
    if _str.isdigit():
        return int(_str)
    return None

def replace_slash(_str):
    return _str.replace('/', '')

def get_first_if_exists(value):
    if value:
        return value[0]
    return None