import os
from flask import Markup,request, Flask, render_template

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
    book = request.form['book']
    print("chapter input: " + str(text) + '. book: ' + str(book))
    try:
        processed_text = int(text)
    except ValueError:
        print("The value entered was incorrect. Setting the chapter to 1")
        processed_text = int(1)

    return get_audioBook_chapter(book_number=int(book), chapter=processed_text)


@app.route('/hpotter/')
def audiobooks():
    # request.form['chapter'] = 2
    return render_template('audiobook.html', navigation=nav,framework=book_number)


@app.route('/hpotter/<book_number>/<chapter>')
def get_audioBook_chapter(book_number=None, chapter=None):
    link = get_download_link(chapter=chapter, book_choice=book_number)

    return render_template('audiobook.html', link=link, chapter=chapter, navigation=nav,framework=book_number)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host= '0.0.0.0', port=9000, debug=False)
    # app.run(debug=True)
