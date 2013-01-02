import re


def validate_username(username):
    if re.match('^\w+$', username):
        return True
    else:
        return False
