import sys, os
import random
import logging
from flask import Flask
from flask import render_template, request
import psycopg2

app = Flask(__name__)

TEXT_COLORS = ('000000', 'ffffff')

WORDS = ['North', 'South', 'East', 'West', 'Table', 'Chair', 'Desk']

DB_CONFIG = dict(host='ec2-54-243-243-182.compute-1.amazonaws.com',
                 database='d7smdsih9vgc05',
                 user='xsbrlpfnutehtr',
                 password='U2OEvQ2SXT0tx2C4XdB3pUiTWp',
                 port=5432
                 )

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

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute('INSERT INTO answers (color, text_color) VALUES (%s, %s);', (color, text_color))
    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)