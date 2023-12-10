import re


def verify_name(room_name):
    p = re.compile('[a-z0-9_]{1,32}')
    m = p.match(room_name)
    if m:
        if m.group() == room_name:
            return m.group()

    return False
