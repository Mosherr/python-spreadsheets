import random
import string


def random_string(string_length=16):
    """
    Generate a random string of fixed length.

    :param int string_length: the length of the random string to generate
    :return a random string
    :rtype: str
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))