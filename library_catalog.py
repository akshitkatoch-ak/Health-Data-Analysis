"""A small command-line library catalog demonstrating classes and inheritance.

Run with ``python library_catalog.py``.
"""

from dataclasses import dataclass
from typing import List, Optional, Sequence


@dataclass
class Book:
    title: str
    author: str
    genre: str
    available: bool = True
    catalog_id: Optional[int] = None

    def display_details(self) -> str:
        status = "Available" if self.available else "Borrowed"
        return (
            f"ID: {self.catalog_id} | Title: {self.title} | "
            f"Author: {self.author} | Genre: {self.genre} | Status: {status}"
        )

    def check_availability(self) -> bool:
        return self.available

    def update_availability(self, available: bool) -> None:
        if not isinstance(available, bool):
            raise TypeError("Availability must be a boolean value.")
        self.available = available


@dataclass
class FictionBook(Book):
    subgenre: str = ""

    def display_details(self) -> str:
        details = super().display_details()
        if self.subgenre:
            details += f" | Subgenre: {self.subgenre}"
        return details


@dataclass
class NonFictionBook(Book):
    subject: str = ""

    def display_details(self) -> str:
        details = super().display_details()
        if self.subject:
            details += f" | Subject: {self.subject}"
        return details


@dataclass
class ReferenceBook(Book):
    reference_section: str = ""

    def display_details(self) -> str:
        details = super().display_details()
        if self.reference_section:
            details += f" | Reference section: {self.reference_section}"
        return details


class LibraryCatalog:
    """Store books and perform catalog, search, and lending operations."""

    def __init__(self) -> None:
        self._books: List[Book] = []
        self._next_id = 1

    @property
    def books(self) -> Sequence[Book]:
        return tuple(self._books)

    def add_book(self, book: Book) -> int:
        if not isinstance(book, Book):
            raise TypeError("Only Book instances can be added to the catalog.")
        if any(existing is book for existing in self._books):
            raise ValueError("This book is already in the catalog.")
        catalog_id = self._next_id
        book.catalog_id = catalog_id
        self._next_id += 1
        self._books.append(book)
        return catalog_id

    def get_book(self, catalog_id: int) -> Book:
        for book in self._books:
            if book.catalog_id == catalog_id:
                return book
        raise ValueError(f"No book found with ID {catalog_id}.")

    def remove_book(self, catalog_id: int) -> Book:
        book = self.get_book(catalog_id)
        self._books = [item for item in self._books if item is not book]
        return book

    def search_by_title(self, query: str) -> List[Book]:
        normalized_query = query.strip().casefold()
        return [
            book
            for book in self._books
            if normalized_query in book.title.casefold()
        ]

    def search_by_author(self, query: str) -> List[Book]:
        normalized_query = query.strip().casefold()
        return [
            book
            for book in self._books
            if normalized_query in book.author.casefold()
        ]

    def get_available_books(self) -> List[Book]:
        return [book for book in self._books if book.check_availability()]

    def borrow_book(self, catalog_id: int) -> None:
        book = self.get_book(catalog_id)
        if not book.check_availability():
            raise ValueError(f'"{book.title}" is already borrowed.')
        book.update_availability(False)

    def return_book(self, catalog_id: int) -> None:
        book = self.get_book(catalog_id)
        if book.check_availability():
            raise ValueError(f'"{book.title}" is already available.')
        book.update_availability(True)

    def display_available_books(self) -> None:
        display_books(self.get_available_books())


def display_books(books: Sequence[Book]) -> None:
    if not books:
        print("No books found.")
        return
    for book in books:
        print(book.display_details())


def _read_required(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This value cannot be empty.")


def _read_book(catalog: LibraryCatalog) -> None:
    book_type = input(
        "Book type (fiction/non-fiction/reference): "
    ).strip().casefold()
    book_types = ("fiction", "non-fiction", "reference")
    if book_type not in book_types:
        print("Unknown book type. Choose fiction, non-fiction, or reference.")
        return

    title = _read_required("Title: ")
    author = _read_required("Author: ")
    genre = _read_required("Genre: ")

    if book_type == "fiction":
        book = FictionBook(
            title, author, genre, subgenre=input("Subgenre (optional): ").strip()
        )
    elif book_type == "non-fiction":
        book = NonFictionBook(
            title, author, genre, subject=input("Subject (optional): ").strip()
        )
    elif book_type == "reference":
        book = ReferenceBook(
            title,
            author,
            genre,
            reference_section=input("Reference section (optional): ").strip(),
        )

    catalog_id = catalog.add_book(book)
    print(f'Added "{book.title}" with catalog ID {catalog_id}.')


def _read_catalog_id() -> Optional[int]:
    raw_id = input("Catalog ID: ").strip()
    try:
        catalog_id = int(raw_id)
    except ValueError:
        print("Enter a whole-number catalog ID.")
        return None
    return catalog_id


def run_cli() -> None:
    catalog = LibraryCatalog()
    actions = {
        "1": "Display all books",
        "2": "Add a book",
        "3": "Search by title",
        "4": "Search by author",
        "5": "Check book availability",
        "6": "Borrow a book",
        "7": "Return a book",
        "8": "Display available books",
        "9": "Remove a book",
        "0": "Exit",
    }

    while True:
        print("\nLibrary Catalog")
        for key, description in actions.items():
            print(f"{key}. {description}")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            return
        if choice == "1":
            display_books(catalog.books)
        elif choice == "2":
            _read_book(catalog)
        elif choice in ("3", "4"):
            query = _read_required("Search for: ")
            results = (
                catalog.search_by_title(query)
                if choice == "3"
                else catalog.search_by_author(query)
            )
            display_books(results)
        elif choice == "8":
            catalog.display_available_books()
        elif choice in ("5", "6", "7", "9"):
            catalog_id = _read_catalog_id()
            if catalog_id is None:
                continue
            try:
                if choice == "5":
                    book = catalog.get_book(catalog_id)
                    status = "available" if book.check_availability() else "borrowed"
                    print(f'"{book.title}" is {status}.')
                elif choice == "6":
                    catalog.borrow_book(catalog_id)
                    print("Book borrowed successfully.")
                elif choice == "7":
                    catalog.return_book(catalog_id)
                    print("Book returned successfully.")
                else:
                    removed = catalog.remove_book(catalog_id)
                    print(f'Removed "{removed.title}" from the catalog.')
            except ValueError as error:
                print(error)
        else:
            print("Invalid option. Choose a number from 0 to 9.")


if __name__ == "__main__":
    run_cli()
