from flask import Markup,request, Flask, render_template
from audiobook_webscraper import *
app = Flask(__name__)


@app.route('/chapter/', methods=['POST'])
def my_form_post():
    text = request.form['chapter']
    processed_text = int(text)
    return get_AudioBooks(number=processed_text)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chapter/')
def AudioBooks():
    return render_template('audiobook.html')

@app.route('/chapter/<number>')
def get_AudioBooks(number=None):
    link = get_download_link(chapter=number)
    return render_template('audiobook.html', link=link, chapter=number)
