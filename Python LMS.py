import datetime
import os
import json


class LMS:
    """
    Library Management System

    Modules:
    1. Display Books
    2. Issue Books
    3. Return Books
    4. Add Books
    5. Search Books
    6. Book Statistics
    """

    def __init__(self, list_of_books, library_name):
        self.library_name = library_name

        # Store files in the same folder as this Python program
        folder_path = os.path.dirname(os.path.abspath(__file__))

        self.list_of_books = os.path.join(folder_path, list_of_books)
        self.data_file = os.path.join(folder_path, "books_data.json")

        self.books_dict = {}

        # Load previously saved book records
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.books_dict = json.load(file)

        # First time: read book names from text file
        else:
            Id = 101

            with open(self.list_of_books, "r") as bk:
                content = bk.readlines()

                for line in content:
                    book_title = line.strip()

                    if book_title:
                        self.books_dict[str(Id)] = {
                            "books_title": book_title,
                            "lender_name": "",
                            "Issue_date": "",
                            "Status": "Available"
                        }

                        Id += 1

            self.save_data()

    # Save book records permanently
    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.books_dict, file, indent=4)

    # Display all books
    def display_books(self):
        print("\n-------------------- List of Books --------------------")
        print("Book ID\t\tTitle\t\t\tStatus")
        print("------------------------------------------------------")

        if not self.books_dict:
            print("No books available.")
            return

        for key, value in self.books_dict.items():
            print(
                key,
                "\t\t",
                value["books_title"],
                "\t\t",
                value["Status"]
            )

    # Issue a book
    def issue_book(self):
        books_id = input("Enter book ID: ").strip()

        if books_id not in self.books_dict:
            print("Book ID not found!")
            return

        book = self.books_dict[books_id]

        if book["Status"] != "Available":
            print(
                f"This book is already issued to "
                f"{book['lender_name']} on {book['Issue_date']}"
            )
            return

        your_name = input("Enter your name: ").strip()

        if your_name == "":
            print("Name cannot be empty!")
            return

        current_date = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        book["lender_name"] = your_name
        book["Issue_date"] = current_date
        book["Status"] = "Already Issued"

        self.save_data()

        print("Book Issued Successfully!")

    # Add a new book
    def add_books(self):
        new_books = input("Enter book title: ").strip()

        if new_books == "":
            print("Book title cannot be empty!")
            return

        if len(new_books) > 25:
            print("Book title should not exceed 25 characters!")
            return

        # Generate the next book ID
        if self.books_dict:
            new_id = max(int(book_id) for book_id in self.books_dict) + 1
        else:
            new_id = 101

        self.books_dict[str(new_id)] = {
            "books_title": new_books,
            "lender_name": "",
            "Issue_date": "",
            "Status": "Available"
        }

        # Add the title to the text file too
        with open(self.list_of_books, "a") as bk:
            bk.write(new_books + "\n")

        self.save_data()

        print(f"Book '{new_books}' added successfully!")
        print(f"New Book ID: {new_id}")

    # Return a book
    def return_books(self):
        books_id = input("Enter book ID: ").strip()

        if books_id not in self.books_dict:
            print("Book ID not found!")
            return

        book = self.books_dict[books_id]

        if book["Status"] == "Available":
            print("This book is already available.")
            return

        book["lender_name"] = ""
        book["Issue_date"] = ""
        book["Status"] = "Available"

        self.save_data()

        print("Book Returned Successfully!")

    # Search books by title
    def search_books(self):
        search_title = input("Enter book title to search: ").strip().lower()

        found = False

        print("\n---------------- Search Results ----------------")

        for key, value in self.books_dict.items():
            if search_title in value["books_title"].lower():
                print(
                    key,
                    "\t",
                    value["books_title"],
                    "\t",
                    value["Status"]
                )
                found = True

        if not found:
            print("No matching books found.")

    # Display book statistics
    def book_statistics(self):
        total_books = len(self.books_dict)

        available_books = sum(
            1 for book in self.books_dict.values()
            if book["Status"] == "Available"
        )

        issued_books = total_books - available_books

        print("\n------------ Book Statistics ------------")
        print("Total Books     :", total_books)
        print("Available Books :", available_books)
        print("Issued Books    :", issued_books)


# Main program
try:
    myLMS = LMS("list_of_books.txt", "Python's Library")

    press_key_list = {
        "D": "Display Books",
        "I": "Issue Books",
        "A": "Add Books",
        "R": "Return Books",
        "S": "Search Books",
        "T": "Book Statistics",
        "Q": "Quit"
    }

    while True:
        print(
            f"\n------------- Welcome To {myLMS.library_name} "
            f"Library Management System -------------"
        )

        for key, value in press_key_list.items():
            print("Press", key, "To", value)

        key_press = input("Press key: ").strip().lower()

        if key_press == "d":
            myLMS.display_books()

        elif key_press == "i":
            myLMS.issue_book()

        elif key_press == "a":
            myLMS.add_books()

        elif key_press == "r":
            myLMS.return_books()

        elif key_press == "s":
            myLMS.search_books()

        elif key_press == "t":
            myLMS.book_statistics()

        elif key_press == "q":
            print("Thank you for using the Library Management System!")
            break

        else:
            print("Invalid key! Please try again.")

except Exception as e:
    print("Something went wrong:", e)