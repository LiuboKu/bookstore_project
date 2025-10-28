import json
from datetime import datetime
from collections import Counter

class Employee:
    def __init__(self, full_name, position, phone, email):
        self.full_name = full_name
        self.position = position
        self.phone = phone
        self.email = email

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Employee(**data)

    def __str__(self):
        return f"{self.full_name} ({self.position}) - {self.phone}, {self.email}"


class Book:
    def __init__(self, title, year, author, genre, cost_price, sale_price):
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre
        self.cost_price = cost_price
        self.sale_price = sale_price

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Book(**data)

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year}) - {self.genre}, {self.sale_price}$"


class Sale:
    def __init__(self, employee_name, book_title, sale_date, real_price):
        self.employee_name = employee_name
        self.book_title = book_title
        self.sale_date = sale_date  # формат YYYY-MM-DD
        self.real_price = real_price

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Sale(**data)

    def __str__(self):
        return f"{self.sale_date}: {self.book_title} продано {self.employee_name} за {self.real_price}$"


# ---------------------- Менеджери ----------------------

class EmployeeManager:
    def __init__(self):
        self.employees = []

    def add_employee(self, emp: Employee):
        self.employees.append(emp)

    def remove_employee(self, full_name):
        self.employees = [e for e in self.employees if e.full_name != full_name]

    def list_employees(self):
        for e in self.employees:
            print(e)

    def to_dict(self):
        return [e.to_dict() for e in self.employees]

    def from_dict(self, data):
        self.employees = [Employee.from_dict(d) for d in data]


class BookManager:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [b for b in self.books if b.title != title]

    def list_books(self):
        for b in self.books:
            print(b)

    def to_dict(self):
        return [b.to_dict() for b in self.books]

    def from_dict(self, data):
        self.books = [Book.from_dict(d) for d in data]


class SaleManager:
    def __init__(self):
        self.sales = []

    def add_sale(self, sale: Sale):
        self.sales.append(sale)

    def remove_sale(self, book_title, sale_date):
        self.sales = [s for s in self.sales if not (s.book_title == book_title and s.sale_date == sale_date)]

    def list_sales(self):
        for s in self.sales:
            print(s)

# ---------------------- Фільтрації ----------------------
    def sales_by_date(self, date_str):
        return [s for s in self.sales if s.sale_date == date_str]

    def sales_by_period(self, start_date, end_date):
        return [s for s in self.sales if start_date <= s.sale_date <= end_date]

    def sales_by_employee(self, employee_name):
        return [s for s in self.sales if s.employee_name == employee_name]

    def most_sold_book(self, start_date, end_date):
        sales = self.sales_by_period(start_date, end_date)
        counter = Counter([s.book_title for s in sales])
        return counter.most_common(1)[0] if counter else None

    def best_employee(self, start_date, end_date):
        sales = self.sales_by_period(start_date, end_date)
        counter = Counter([s.employee_name for s in sales])
        return counter.most_common(1)[0] if counter else None

    def total_profit(self, start_date, end_date, book_manager: BookManager):
        sales = self.sales_by_period(start_date, end_date)
        profit = 0
        for s in sales:
            book = next((b for b in book_manager.books if b.title == s.book_title), None)
            if book:
                profit += s.real_price - book.cost_price
        return profit

    def most_sold_author(self, start_date, end_date, book_manager: BookManager):
        sales = self.sales_by_period(start_date, end_date)
        authors = [next((b.author for b in book_manager.books if b.title == s.book_title), None) for s in sales]
        counter = Counter(authors)
        return counter.most_common(1)[0] if counter else None

    def most_sold_genre(self, start_date, end_date, book_manager: BookManager):
        sales = self.sales_by_period(start_date, end_date)
        genres = [next((b.genre for b in book_manager.books if b.title == s.book_title), None) for s in sales]
        counter = Counter(genres)
        return counter.most_common(1)[0] if counter else None

    def to_dict(self):
        return [s.to_dict() for s in self.sales]

    def from_dict(self, data):
        self.sales = [Sale.from_dict(d) for d in data]


# ---------------------- Функції для збереження/завантаження ----------------------

def save_data(employee_mgr, book_mgr, sale_mgr, filename="data.json"):
    data = {
        "employees": employee_mgr.to_dict(),
        "books": book_mgr.to_dict(),
        "sales": sale_mgr.to_dict()
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(employee_mgr, book_mgr, sale_mgr, filename="data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        employee_mgr.from_dict(data.get("employees", []))
        book_mgr.from_dict(data.get("books", []))
        sale_mgr.from_dict(data.get("sales", []))
    except FileNotFoundError:
        print("Файл даних не знайдено. Створюємо нову базу.")




def main():
    emp_mgr = EmployeeManager()
    book_mgr = BookManager()
    sale_mgr = SaleManager()

    load_data(emp_mgr, book_mgr, sale_mgr)

    # Для прикладу додамо кілька записів
    emp_mgr.add_employee(Employee("Іван Іванов", "Продавець", "0501234567", "ivan@mail.com"))
    book_mgr.add_book(Book("Python для початківців", 2022, "Петренко Петро", "Програмування", 10, 20))
    sale_mgr.add_sale(Sale("Іван Іванов", "Python для початківців", "2025-10-25", 22))

    # Приклад звіту
    print("\nВсі продажі:")
    sale_mgr.list_sales()

    most_book = sale_mgr.most_sold_book("2025-10-01", "2025-10-31")
    print("\nНайбільш продавана книга за жовтень 2025:", most_book)

    profit = sale_mgr.total_profit("2025-10-01", "2025-10-31", book_mgr)
    print("Сумарний прибуток за жовтень 2025:", profit, "$")

    save_data(emp_mgr, book_mgr, sale_mgr)

main()