class Book: #წიგნის კლასი რომელსაც აქვს ინსთენს ატრიბუტები სათაურის, ავტორის და გამოშვების წლისათვის
    def __init__(self, title: str, author: str, year: int): #ინსთენს ატრიბუტების ინიციალიზაცია კონსტრუქტორით
        self._title = title
        self._author = author
        self._year = year

    @property #ვქმნით იმისათვის რომ გავაკონტროლოთ და შევამოწმოთ მონაცემები
    def title(self):
        return self._title
 
    @title.setter #მონაცემის შესაყვანი
    def title(self, value):
        if not value.strip():
            raise ValueError("Title cannot be empty.")
        self._title = value
 
    @property #მონაცემის მიმღები
    def author(self):
        return self._author
 
    @author.setter 
    def author(self, value):
        if not value.strip():
            raise ValueError("Author cannot be empty.")
        self._author = value
 
    @property
    def year(self):
        return self._year
 
    @year.setter
    def year(self, value):
        if not isinstance(value, int):
            raise ValueError("Year cannot be empty and it must be a positive integer.")
        self._year = value
 
    def display_info(self): #ვქმნით იმისათვის რომ კიდევ გამოვიყენოთ
        return f"Title: {self.title} | Author: {self.author} | Year: {self.year}"
 
    def __str__(self):
        return self.display_info()
 
 
class BookManager:  #ვქმნით კლასს რომელიც მართავს წიგნებს
    def __init__(self):
        self._books = []
 
    def add_book(self, book: Book): #ვქმნით მეთოდს რომელიც დაამატებს წიგნს ბიბლიოთეკაში
        self._books.append(book)
 
    def get_all_books(self): #გამოგვაქვს მთლიანი ბიბლიოთეკა
        return list(self._books)
 
    def search_by_title(self, title_query: str): #სარჩევი სათაურის მიხედვით
        title_query = title_query.lower()
        return [book for book in self._books if title_query in book.title.lower()]

 
def input_non_empty(userinp: str): #ვამოწმებთ აკმაყოფილებს თუ არა ინფუთი მოთხოვნებს
    while True:
        value = input(userinp).strip()
        if value:
            return value
        else:
            print("Input cannot be empty.")
 
 
def input_year(userinp: str): #შეყვანილი წელი უნდა იყოს დადებითი რიცხვი
    while True:
        text = input(userinp).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("Invalid year. Year must be a positive integer.")
 
 
def print_menu(): #კონსოლის მენიუ რომელიც იქნება პირველი რასაც მომხმარებელი დაინახავს
    print("\n=== BOOK MANAGEMENT SYSTEM ===")
    print("1. Add a new book")
    print("2. View all books")
    print("3. Search for a book by title")
    print("0. Exit")
 
 
def add_book_cnsl(manager: BookManager): #ბუქმენეჯერ კლასის მეთოდს ვიყენებთ კონსოლიდან წიგნის დასამატებლად
    title = input_non_empty("Enter title: ")
    author = input_non_empty("Enter author: ")
    year = input_year("Enter year of publication: ")
    manager.add_book(Book(title, author, year))
    print("Book added successfully.")
 
 
def view_books_cnsl(manager: BookManager): #ბუქმენეჯერ კლასის მეთოდს ვიყენებთ კონსოლიდან მთლიანი ბიბლიოთეკის სანახავად
    books = manager.get_all_books()
    if not books:
        print("There are no books yet. Add the books first!")
        return
    for i, j in enumerate(books, start=1):
        print(f"{i}. {j.display_info()}")
 
 
def search_book_cnsl(manager: BookManager): #კლასის მეთოდს ვიყენებთ კონსოლიდან წიგნის მოსაძებნად
    query = input_non_empty("Enter title or part of title: ")
    results = manager.search_by_title(query)
    if not results:
        print("No books found.")
        return
    for index, book in enumerate(results, start=1):
        print(f"{index}. {book.display_info()}")
 
 
def main(): #მთავარი ფუნქცია რომელიც ამუშავებს პროგრამას და აკონტროლებს კონსოლისდან იუზერის ინტერაქციას
    manager = BookManager()
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_book_cnsl(manager)
        elif choice == "2":
            view_books_cnsl(manager)
        elif choice == "3":
            search_book_cnsl(manager)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
 
 
if __name__ == "__main__": #უშვებს მეინ ფუნქციას როცა სკრიპტი პირდაპირ არის გაშვებული ადგილობრივად.
    main()
 