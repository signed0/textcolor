import struct
import random

class ColorError(Exception):
    pass

def decode_hex_color(hex_str):
    return struct.unpack('BBB',hex_str.decode('hex'))    

def validate_color(color):
    if not color:
        raise ColorError("Color is empty")

    color = color.strip().lower()

    if len(color) != 6:
        raise ColorError("Color is not proper length")

    for c in color:
        if c not in '0123456789abcdef':
            raise ColorError("Invalid color character %s" % c)

    return color

def random_color():
    return ''.join(random.choice('0123456789abcdef') for _ in range(6))