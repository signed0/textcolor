import random
import struct
from colorsys import rgb_to_hsv

from flask import render_template, request

import psycopg2
from app import app

from utils import parse_db_uri

TEXT_COLORS = ('000000', 'ffffff')

WORDS = ['North', 'South', 'East', 'West', 'Table', 'Chair', 'Desk']

def db_conn(app):
    db_params = parse_db_uri(app.config['DATABASE_URI'])

    assert db_params['adapter'] == 'postgres'
    del db_params['adapter']

    return psycopg2.connect(**db_params)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        color = request.form.get('color')
        text_color = request.form.get('text_color')

        if text_color in TEXT_COLORS:
            record_response(color, text_color)
        elif text_color == 'toss_up':
            record_response(color, None)

    color = random_color()

    text_colors = list(TEXT_COLORS)
    random.shuffle(text_colors)
    left_color, right_color = text_colors
    word = random.choice(WORDS)

    return render_template('index.html', 
                           color=color,
                           left_color=left_color,
                           right_color=right_color,
                           word=word
                           )

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

def record_response(color, text_color):
    try:
        color = validate_color(color)        
        if text_color is not None:
            text_color = validate_color(text_color)
    except Exception as e:
        logging.exception(e)
        return

    rgb = decode_hex_color(color)
    rgb = tuple(i / 255.0 for i in rgb)
    h, s, v = rgb_to_hsv(*rgb)

    h = int(round(h * 360))
    s = int(round(s * 100))
    v = int(round(v * 100))

    conn = db_conn(app)
    cur = conn.cursor()

    sql = '''INSERT INTO answers (color, text_color, color_h, color_s, color_v) 
                VALUES (%s, %s, %s, %s, %s);'''
    cur.execute(sql, (color, text_color, h, s, v))
    conn.commit()

    cur.close()
    conn.close()
