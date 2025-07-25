from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# Global data structure to store books
library = {}

def validateISBN(isbn):
    """
    Validates the ISBN using a regular expression.
    Supports:
    - ISBN-10: Format (e.g., 12-1234-123-1)
    - ISBN-13: Formats (e.g., 978-0-618-26030-0, 978-93-96055-02-6)
    """
    pattern = r'^(\d{2}-\d{4}-\d{3}-\d{1}|978-\d{1,2}-\d{3,5}-\d{2}-\d{1})$'
    return bool(re.match(pattern, isbn))

@app.route('/')
def home():
    return render_template('index.html', library=library)

@app.route('/add', methods=['POST'])
def add_book():
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    if validateISBN(isbn):
        if isbn in library:
            return "Book with this ISBN already exists.", 400
        else:
            library[isbn] = title
            return redirect(url_for('home'))
    else:
        return "Invalid ISBN. Please try again.", 400

@app.route('/search', methods=['GET'])
def search_book():
    isbn = request.args.get('isbn')
    if isbn in library:
        return f"Book Found: {library[isbn]}"
    else:
        return "Book not found.", 404

@app.route('/remove', methods=['POST'])
def remove_book():
    isbn = request.form.get('isbn')
    if isbn in library:
        del library[isbn]
        return redirect(url_for('home'))
    else:
        return "Book not found.", 404

if __name__ == "__main__":
    app.run(debug=True)