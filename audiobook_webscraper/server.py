import os
from flask import Markup,request, Flask, render_template
# from flask import flash, redirect,request, session, abort

from audiobook_webscraper import *

app = Flask(__name__)

app.static_folder = 'static'

nav=[{'caption': 'Home','href': '/'}, {'caption': 'Harry Potter', 'href': '/hpotter'}]

@app.route('/')
def home():
    return render_template('home.html', navigation=nav)


@app.route('/hpotter/', methods=['POST'])
def my_form_post():
    text = request.form['chapter']
    print("text input: " + str(text))
    try:
        processed_text = int(text)
    except ValueError:
        print("The value entered was incorrect. Setting the chapter to 1")
        processed_text = int(1)
    return get_audioBook_chapter(number=processed_text)


@app.route('/hpotter/')
def audiobooks():
    return render_template('audiobook.html', navigation=nav)

@app.route('/hpotter/<number>')
def get_audioBook_chapter(number=None):
    link = get_download_link(chapter=number)
    return render_template('audiobook.html', link=link, chapter=number, navigation=nav)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host= '0.0.0.0', port=9000, debug=False)
    # app.run(debug=True)
