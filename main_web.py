import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_for_production'
DATABASE = 'library.db'

# --- Database Setup ---
def init_db():
    """Initializes the database and creates the books table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            isbn TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Flask Routes ---
@app.route('/')
def home():
    """Displays all books from the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY title")
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    """Adds a new book to the database."""
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')

    # Basic validation
    if not all([isbn, title, author, year]):
        flash("Error: All fields are required.", 'danger')
        return redirect(url_for('home'))

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (isbn, title, author, year) VALUES (?, ?, ?, ?)",
                       (isbn, title, author, year))
        conn.commit()
        flash("Success: Book added to the library!", 'success')
    except sqlite3.IntegrityError:
        flash(f"Error: Book with ISBN '{isbn}' already exists.", 'danger')
    except Exception as e:
        flash(f"An error occurred: {e}", 'danger')
    finally:
        if conn:
            conn.close()

    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_book():
    """Updates an existing book's details."""
    original_isbn = request.form.get('original_isbn')
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')

    if not all([original_isbn, title, author, year]):
        flash("Error: All fields are required for an update.", 'danger')
        return redirect(url_for('home'))

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE isbn = ?",
                       (title, author, year, original_isbn))
        conn.commit()
        flash("Success: Book details have been updated.", 'success')
    except Exception as e:
        flash(f"An error occurred during update: {e}", 'danger')
    finally:
        if conn:
            conn.close()

    return redirect(url_for('home'))


@app.route('/remove/<string:isbn>', methods=['POST'])
def remove_book(isbn):
    """Removes a book from the database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        conn.commit()
        flash("Success: Book removed from the library.", 'success')
    except Exception as e:
        flash(f"An error occurred: {e}", 'danger')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('home'))


if __name__ == "__main__":
    init_db()  # Ensure the database and table exist before running the app
    app.run(debug=True)