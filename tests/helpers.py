import random


def random_unicode_char():
    # Unicode code points range from 0 to 0x10FFFF
    code_point = random.randint(0, 0x10FFFF)
    # Exclude surrogate pairs (0xD800–0xDFFF) as they are not valid Unicode characters
    while 0xD800 <= code_point <= 0xDFFF:
        code_point = random.randint(0, 0x10FFFF)
    return chr(code_point)


def random_utf8_string(min_length=1, max_length=100):
    # Determine the length of the string
    length = random.randint(min_length, max_length)
    # Generate a list of random Unicode characters
    random_chars = [random_unicode_char() for _ in range(length)]
    # Join the list into a single string
    return ''.join(random_chars)
