import json
from datetime import datetime
from collections import Counter

# ---------------------- Класи ----------------------

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
        return Employee(
            data.get("full_name", ""),
            data.get("position", ""),
            data.get("phone", ""),
            data.get("email", "")
        )

    def __str__(self):
        return f"{self.full_name} ({self.position}) - {self.phone}, {self.email}"


class Book:
    _id_counter = 1

    def __init__(self, title, year, author, genre, cost_price, sale_price):
        self.id = Book._id_counter
        Book._id_counter += 1
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
        title = data.get('title', '')
        year = data.get('year', 0)
        author = data.get('author', '')
        genre = data.get('genre', '')
        cost_price = data.get('cost_price', 0.0)
        sale_price = data.get('sale_price', 0.0)

        book = Book(title, year, author, genre, cost_price, sale_price)
        if isinstance(data.get('id'), int):
            book.id = data['id']
            if book.id >= Book._id_counter:
                Book._id_counter = book.id + 1
        return book

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.author}, {self.year}) - {self.genre}, {self.sale_price}$"


class Sale:
    def __init__(self, employee_name, book_id, sale_date, real_price):
        self.employee_name = employee_name
        self.book_id = book_id
        self.sale_date = sale_date
        self.real_price = real_price

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Sale(
            data.get('employee_name', ''),
            data.get('book_id', None),
            data.get('sale_date', ''),
            data.get('real_price', 0.0)
        )

    def __str__(self):
        book_part = f"Книга ID {self.book_id}" if self.book_id is not None else "Книга (невідомий ID)"
        return f"{self.sale_date}: {book_part} продано {self.employee_name} за {self.real_price}$"


# ---------------------- Менеджери ----------------------

class EmployeeManager:
    def __init__(self):
        self.employees = []

    def add_employee(self, emp: Employee):
        self.employees.append(emp)

    def remove_employee(self, full_name):
        self.employees = [e for e in self.employees if e.full_name != full_name]

    def list_employees(self):
        if not self.employees:
            print("Список працівників порожній.")
        for e in self.employees:
            print(e)

    def find_employee(self, full_name):
        return next((e for e in self.employees if e.full_name.lower() == full_name.lower()), None)

    def to_dict(self):
        return [e.to_dict() for e in self.employees]

    def from_dict(self, data):
        self.employees = [Employee.from_dict(d) for d in data]


class BookManager:
    def __init__(self):
        self.books = []

    def list_books(self):
        if not self.books:
            print("Список книг порожній.")
        for b in self.books:
            print(b)

    def find_book(self, book_id):
        return next((b for b in self.books if b.id == book_id), None)

    def to_dict(self):
        return [b.to_dict() for b in self.books]

    def from_dict(self, data):
        self.books = [Book.from_dict(d) for d in data]


class SaleManager:
    def __init__(self):
        self.sales = []

    def add_sale(self, sale):
        self.sales.append(sale)

    def remove_sale(self, book_id, sale_date):
        self.sales = [s for s in self.sales if not (s.book_id == book_id and s.sale_date == sale_date)]

    def list_sales(self):
        if not self.sales:
            print("Список продажів порожній.")
        for s in self.sales:
            print(s)

    def sales_by_period(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("Невірний формат дати! Використовуйте YYYY-MM-DD.")
            return []

        result = []
        for s in self.sales:
            try:
                sale_dt = datetime.strptime(s.sale_date, "%Y-%m-%d")
                if start <= sale_dt <= end:
                    result.append(s)
            except ValueError:
                print(f"Продаж {s.book_id} має некоректну дату: {s.sale_date}")
        return result

    def most_sold_book(self, start_date, end_date):
        sales = self.sales_by_period(start_date, end_date)
        counter = Counter([s.book_id for s in sales if s.book_id is not None])
        return counter.most_common(1)[0] if counter else None

    def best_employee(self, start_date, end_date):
        sales = self.sales_by_period(start_date, end_date)
        counter = Counter([s.employee_name for s in sales])
        return counter.most_common(1)[0] if counter else None

    def total_profit(self, start_date, end_date, book_manager):
        sales = self.sales_by_period(start_date, end_date)
        profit = 0
        for s in sales:
            book = next((b for b in book_manager.books if b.id == s.book_id), None)
            if book:
                profit += s.real_price - book.cost_price
        return profit

    def most_sold_author(self, start_date, end_date, book_manager):
        sales = self.sales_by_period(start_date, end_date)
        authors = [
            next((b.author for b in book_manager.books if b.id == s.book_id), None)
            for s in sales
        ]
        counter = Counter([a for a in authors if a is not None])
        return counter.most_common(1)[0] if counter else None

    def most_sold_genre(self, start_date, end_date, book_manager):
        sales = self.sales_by_period(start_date, end_date)
        genres = [
            next((b.genre for b in book_manager.books if b.id == s.book_id), None)
            for s in sales
        ]
        counter = Counter([g for g in genres if g is not None])
        return counter.most_common(1)[0] if counter else None

    def to_dict(self):
        return [s.to_dict() for s in self.sales]

    def from_dict(self, data):
        self.sales = [Sale.from_dict(d) for d in data]


# ---------------------- Клас для дій з книгами ----------------------

class BookActions:
    def __init__(self, book_manager: BookManager):
        self.book_manager = book_manager

    def add_book(self):
        title = input("Назва: ")
        year = self.get_valid_year("Рік видання: ")
        author = input("Автор: ")
        genre = input("Жанр: ")
        cost_price = self.get_valid_float("Собівартість: ")
        sale_price = self.get_valid_float("Ціна продажу: ")
        book = Book(title, year, author, genre, cost_price, sale_price)
        self.book_manager.books.append(book)
        print(f"Книгу [{book.id}] додано!")

    def remove_book(self):
        book_id = self.get_valid_int("Введіть ID книги для видалення: ")
        before = len(self.book_manager.books)
        self.book_manager.books = [b for b in self.book_manager.books if b.id != book_id]
        after = len(self.book_manager.books)
        if before == after:
            print(f"Книга з ID {book_id} не знайдена.")
        else:
            print(f"Книгу [{book_id}] видалено!")

    @staticmethod
    def get_valid_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Будь ласка, введіть ціле число!")

    @staticmethod
    def get_valid_float(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Будь ласка, введіть число!")

    @staticmethod
    def get_valid_year(prompt):
        current_year = datetime.now().year
        while True:
            try:
                year = int(input(prompt))
                if 1400 <= year <= current_year:
                    return year
                else:
                    print(f"Рік повинен бути в межах 1400 - {current_year}.")
            except ValueError:
                print("Будь ласка, введіть правильний рік!")


# ---------------------- Збереження/завантаження ----------------------

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
            raw = json.load(f)
    except FileNotFoundError:
        print("Файл даних не знайдено. Створюємо нову базу.")
        return

    employee_mgr.from_dict(raw.get("employees", []))
    book_mgr.from_dict(raw.get("books", []))

    sales_raw = raw.get("sales", [])
    sales_objs = []
    for s in sales_raw:
        book_id = s.get('book_id')
        if book_id is None and 'book_title' in s:
            found = next((b for b in book_mgr.books if b.title == s['book_title']), None)
            book_id = found.id if found else None
        sale_obj = Sale(
            s.get('employee_name', ''),
            book_id,
            s.get('sale_date', ''),
            s.get('real_price', 0.0)
        )
        sales_objs.append(sale_obj)
    sale_mgr.sales = sales_objs


# ---------------------- Інтерактивне меню ----------------------

def main():
    emp_mgr = EmployeeManager()
    book_mgr = BookManager()
    sale_mgr = SaleManager()
    book_actions = BookActions(book_mgr)

    load_data(emp_mgr, book_mgr, sale_mgr)

    while True:
        print("\n--- Меню книжкового магазину ---")
        print("1. Працівники")
        print("2. Книги")
        print("3. Продажі")
        print("4. Звіти")
        print("5. Вийти")
        choice = input("Виберіть опцію: ")

        if choice == "1":
            print("\n--- Працівники ---")
            print("1. Додати працівника")
            print("2. Видалити працівника")
            print("3. Показати всіх працівників")
            sub_choice = input("Виберіть опцію: ")
            if sub_choice == "1":
                name = input("Ім'я: ")
                pos = input("Посада: ")
                phone = input("Телефон: ")
                email = input("Email: ")
                emp_mgr.add_employee(Employee(name, pos, phone, email))
                print("Працівника додано!")
            elif sub_choice == "2":
                name = input("Ім'я працівника для видалення: ")
                emp_mgr.remove_employee(name)
                print("Працівника видалено!")
            elif sub_choice == "3":
                emp_mgr.list_employees()

        elif choice == "2":
            print("\n--- Книги ---")
            print("1. Додати книгу")
            print("2. Видалити книгу")
            print("3. Показати всі книги")
            sub_choice = input("Виберіть опцію: ")
            if sub_choice == "1":
                book_actions.add_book()
            elif sub_choice == "2":
                book_actions.remove_book()
            elif sub_choice == "3":
                book_mgr.list_books()

        elif choice == "3":
            print("\n--- Продажі ---")
            print("1. Додати продаж")
            print("2. Видалити продаж")
            print("3. Показати всі продажі")
            sub_choice = input("Виберіть опцію: ")
            if sub_choice == "1":
                emp_name = input("Продавець: ")
                employee = emp_mgr.find_employee(emp_name)
                if not employee:
                    print(f"Працівник '{emp_name}' не знайдений.")
                    continue

                book_id = book_actions.get_valid_int("ID книги: ")
                book = book_mgr.find_book(book_id)
                if not book:
                    print(f"Книга з ID {book_id} не знайдена.")
                    continue

                date = input("Дата продажу (YYYY-MM-DD): ")
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    print("Невірний формат дати.")
                    continue

                real_price = book_actions.get_valid_float("Фактична ціна: ")
                sale_mgr.add_sale(Sale(emp_name, book_id, date, real_price))
                print("Продаж додано!")

            elif sub_choice == "2":
                book_id = book_actions.get_valid_int("ID книги: ")
                date = input("Дата продажу (YYYY-MM-DD): ")
                sale_mgr.remove_sale(book_id, date)
                print("Продаж видалено!")

            elif sub_choice == "3":
                sale_mgr.list_sales()

        elif choice == "4":
            print("\n--- Звіти ---")
            start_date = input("Початкова дата (YYYY-MM-DD): ")
            end_date = input("Кінцева дата (YYYY-MM-DD): ")
            most_book = sale_mgr.most_sold_book(start_date, end_date)
            best_emp = sale_mgr.best_employee(start_date, end_date)
            profit = sale_mgr.total_profit(start_date, end_date, book_mgr)
            most_author = sale_mgr.most_sold_author(start_date, end_date, book_mgr)
            most_genre = sale_mgr.most_sold_genre(start_date, end_date, book_mgr)

            print("\nНайбільш продавана книга:", most_book)
            print("Найуспішніший працівник:", best_emp)
            print("Сумарний прибуток:", profit, "$")
            print("Найпопулярніший автор:", most_author)
            print("Найпопулярніший жанр:", most_genre)

        elif choice == "5":
            save_data(emp_mgr, book_mgr, sale_mgr)
            print("Дані збережено. Вихід...")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


main()