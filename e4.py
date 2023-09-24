import sqlite3

# 连接到数据库，如果不存在则创建它
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 创建三个表：Books、Users 和 Reservations
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate DATE,
        FOREIGN KEY (BookID) REFERENCES Books(BookID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
''')

# 提交更改并关闭数据库连接
conn.commit()
conn.close()

def add_book(book_id, title, author, isbn):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)',
                   (book_id, title, author, isbn, 'Available'))
    conn.commit()
    conn.close()
    print(f"Book with ID {book_id} has been added to the library.")

def find_book_details(identifier):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    if identifier.startswith('LB'):
        cursor.execute('''
            SELECT Books.*, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?
        ''', (identifier,))
    elif identifier.startswith('LU'):
        cursor.execute('SELECT * FROM Users WHERE UserID = ?', (identifier,))
    elif identifier.startswith('LR'):
        cursor.execute('SELECT * FROM Reservations WHERE ReservationID = ?', (identifier,))
    else:
        print("Invalid input. Please enter a valid BookID, UserID, or ReservationID.")
        return

    result = cursor.fetchall()
    conn.close()

    if result:
        for row in result:
            print(row)
    else:
        print(f"No record found for {identifier}")

def find_all_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Books.*, Users.Name, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')
    result = cursor.fetchall()
    conn.close()

    if result:
        for row in result:
            print(row)
    else:
        print("No books found in the library.")

def update_book_details(book_id, new_title, new_author, new_isbn, new_status):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Books
        SET Title=?, Author=?, ISBN=?, Status=?
        WHERE BookID=?
    ''', (new_title, new_author, new_isbn, new_status, book_id))
    conn.commit()
    conn.close()
    print(f"Book with ID {book_id} has been updated.")

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Books WHERE BookID=?', (book_id,))
    cursor.execute('DELETE FROM Reservations WHERE BookID=?', (book_id,))
    conn.commit()
    conn.close()
    print(f"Book with ID {book_id} has been deleted.")

# 主程序循环，接受用户输入并执行相应的操作
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find book details by ID")
    print("3. Find book reservation status")
    print("4. Find all books")
    print("5. Update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        book_id = input("Enter BookID: ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        isbn = input("Enter ISBN: ")
        add_book(book_id, title, author, isbn)

    elif choice == '2':
        identifier = input("Enter BookID, UserID, or ReservationID: ")
        find_book_details(identifier)

    elif choice == '3':
        book_id = input("Enter BookID: ")
        find_book_details(book_id)

    elif choice == '4':
        find_all_books()

    elif choice == '5':
        book_id = input("Enter BookID: ")
        new_title = input("Enter new title (leave blank to keep existing): ")
        new_author = input("Enter new author (leave blank to keep existing): ")
        new_isbn = input("Enter new ISBN (leave blank to keep existing): ")
        new_status = input("Enter new status (leave blank to keep existing): ")
        update_book_details(book_id, new_title, new_author, new_isbn, new_status)

    elif choice == '6':
        book_id = input("Enter BookID: ")
        delete_book(book_id)

    elif choice == '7':
        print("Exiting Library Management System.")
        break

    else:
        print("Invalid choice. Please enter a valid option.")
