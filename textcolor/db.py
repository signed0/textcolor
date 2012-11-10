from colorsys import rgb_to_hsv
from color_utils import decode_hex_color

from psycopg2.extras import DictCursor

def get_answers_by_hue(conn, hue):
    cur = conn.cursor(cursor_factory=DictCursor)

    cur.execute("SELECT * from answers WHERE color_h=%s", (hue, ))
    rows = list(cur.fetchall())

    cur.close()

    return rows

def add_answer(conn, color, text_color):
    rgb = decode_hex_color(color)
    rgb = tuple(i / 255.0 for i in rgb)
    h, s, v = rgb_to_hsv(*rgb)

    h = int(round(h * 360))
    s = int(round(s * 100))
    v = int(round(v * 100))

    cur = conn.cursor()

    sql = '''INSERT INTO answers (color, text_color, color_h, color_s, color_v) 
                VALUES (%s, %s, %s, %s, %s);'''
    cur.execute(sql, (color, text_color, h, s, v))
    conn.commit()

    cur.close()    