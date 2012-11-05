import os
import random
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

TEXT_COLORS = ('00000', 'ffffff')

WORDS = ['North', 'South', 'East', 'West']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        color = request.form.get('color')
        text_color = request.form.get('text_color')

        if text_color in TEXT_COLORS:
            record_response(color, text_color)

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

def validate_color(c):
    if not color:
        raise "Color is empty"

    color = color.strip().lower()

    if len(color) != 6:
        raise "Color is not proper length"

    for c in color:
        if c not in '123456789abcdef':
            raise "Invalid color character"            

    return color

def random_color():
    return ''.join(random.choice('123456789abcdef') for _ in range(6))

def record_response(color, text_color):
    try:
        color = validate_color(color)
        text_color = validate_color(text_color)
    except:
        pass


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)