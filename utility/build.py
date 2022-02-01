import random
import string


def build_id():
    return ''.join([random.choice(string.ascii_letters + string.digits)
                    for n in range(16)])
