import re

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

def validateISBNChecksum(isbn):
    # Remove dashes for processing
    isbn_digits = re.sub(r'[^0-9X]', '', isbn)

    if len(isbn_digits) == 10:
        total = 0
        for i in range(9):
            if not isbn_digits[i].isdigit():
                return False
            total += int(isbn_digits[i]) * (10 - i)
        checksum = isbn_digits[9]
        if checksum == 'X':
            total += 10
        elif checksum.isdigit():
            total += int(checksum)
        else:
            return False
        return total % 11 == 0

    elif len(isbn_digits) == 13:
        total = 0
        for i in range(12):
            if not isbn_digits[i].isdigit():
                return False
            total += int(isbn_digits[i]) * (1 if i % 2 == 0 else 3)
        if not isbn_digits[12].isdigit():
            return False
        total += int(isbn_digits[12])
        return total % 10 == 0

    return False
  


def add_book():
    isbn = input("Enter ISBN to add: ")
    if validateISBN(isbn) and validateISBNChecksum(isbn):
        if isbn in library:
            print("Book with this ISBN already exists.")
        else:
            title = input("Enter book title: ")
            library[isbn] = title
            print("Book added successfully.")
    else:
        print("Invalid ISBN. Please try again.")

def search_book():
    isbn = input("Enter ISBN to search: ")
    if isbn in library:
        print(f"Book Found: {library[isbn]}")
    else:
        print("Book not found.")

def show_all_books():
    if library:
        print("Books in Library:")
        for isbn, title in library.items():
            print(f"ISBN: {isbn}, Title: {title}")
    else:
        print("No books in the library.")

def remove_book():
    isbn = input("Enter ISBN to remove: ")
    if isbn in library:
        del library[isbn]
        print("Book removed successfully.")
    else:
        print("Book not found.")

def menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Show All Books")
        print("4. Remove Book")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            search_book()
        elif choice == '3':
            show_all_books()
        elif choice == '4':
            remove_book()
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()