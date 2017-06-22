import os
import IOFunctions

def main():
    books = ["genesis", "exodus", "leviticus", "numbers", "deuteronomy"]

    # create directory for storing books
    if not os.path.exists("Books/"):
        os.makedirs("Books/")

    for book in books:
        IOFunctions.copyBook(book)

if __name__ == '__main__': main()