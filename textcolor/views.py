import random
from operator import itemgetter

from flask import render_template, request, abort

import psycopg2

from app import app
import db
from utils import parse_db_uri
from color_utils import random_color, validate_color, ColorError

TEXT_COLORS = ('000000', 'ffffff')

WORDS = ['North', 'South', 'East', 'West', 'Table', 'Chair', 'Desk', 'Lamp']

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

@app.route('/hues/<int:hue>')
def by_hue(hue):

    if hue < 0 or hue > 360:
        abort(404)

    conn = db_conn(app)
    answers = db.get_answers_by_hue(conn, hue)
    conn.close()

    answers = sorted(answers, key=itemgetter('color_s'))

    return render_template('by_hue.html',
                           hue=hue,
                           answers=answers
                           )

def record_response(color, text_color):
    try:
        color = validate_color(color)        
        if text_color is not None:
            text_color = validate_color(text_color)
    except ColorError as e:
        logging.exception(e)
        return

    conn = db_conn(app)
    db.add_answer(conn, color, text_color)
    conn.close()
