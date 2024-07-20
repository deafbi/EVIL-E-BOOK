from flask import Flask, render_template, send_file
import os
import random
from PyPDF2 import PdfReader
import re

app = Flask(__name__)

def get_books():
    books = [] 
    for series in os.listdir('library'):
        if os.path.isdir(os.path.join('library', series)):
            for book in os.listdir(os.path.join('library', series)):
                if book.endswith('.pdf'):
                    filename = os.path.splitext(book)[0]  # remove .pdf extension
                    title = re.sub(r'^Book\d+', '', str(filename))
                    title = title.replace("-", " ")
                    if len(title) > 23:
                        title = title.strip()[:23] + '...'  # remove "Book" followed by a number
                    path = os.path.join('library', series, book)
                    if "Book" in str(title):
                        pass
                    books.append({
                        'title': title,
                        'series': series,
                        'book': book,
                        'preview': random_color()
                    })
    return books




import random

def random_color():
    # Generate a random color gradient
    r1, g1, b1 = [random.randint(54, 200) for _ in range(3)]  # limits brightness to a range of 54-200
    r2, g2, b2 = [random.randint(54, 200) for _ in range(3)]
    return f"linear-gradient(to right, rgba({r1}, {g1}, {b1}, 1), rgba({r2}, {g2}, {b2}, 1))"


@app.route('/')
def index():
    books = get_books()
    return render_template('index.html', books=books)

@app.route('/read/<series>/<book>')
def read_book(series, book):
    path = os.path.join('library', series, book)
    return send_file(path, download_name=book, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
