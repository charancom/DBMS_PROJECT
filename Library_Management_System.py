import mysql.connector
import streamlit as st
import pandas as pd
import datetime
from datetime import datetime, timedelta

def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Hello@123",
        database="StudentManagement"
    )

def add_new_book(book_title, author_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO library_management (book_title, author_name) VALUES (%s, %s)"
    cursor.execute(query, (book_title, author_name))
    conn.commit()
    print("Book added successfully.")
    cursor.close()
    conn.close()
    st.success("Book added successfully.")


def remove_book(book_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "DELETE FROM library_management WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    conn.commit()
    print("Book removed successfully.")
    cursor.close()
    conn.close()
    st.success("Book removed successfully.")


def update_book_info(book_id, book_title=None, author_name=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    if book_title:
        cursor.execute("UPDATE library_management SET book_title = %s WHERE book_id = %s", (book_title, book_id))
    if author_name:
        cursor.execute("UPDATE library_management SET author_name = %s WHERE book_id = %s", (author_name, book_id))
    conn.commit()
    print("Book information updated successfully.")
    cursor.close()
    conn.close()
    st.success("Book updated info successfully.")


def list_all_books():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch data from the library_management table
    query = """
    SELECT book_id, book_title, author_name, srn, date_borrowed, due_date, return_date, penalty_amount, penalty_days 
    FROM library_management
    """
    cursor.execute(query)
    books = cursor.fetchall()
    cursor.close()
    conn.close()


    # Define column names to match the schema
    columns = ["Book ID", "Book Title", "Author Name", "SRN", "Date Borrowed", "Due Date", "Return Date", "Penalty Amount", "Penalty Days"]

    # Convert to DataFrame and display in Streamlit
    if books:
        books_df = pd.DataFrame(books, columns=columns)
        st.dataframe(books_df)  # Display DataFrame in Streamlit as a table
    else:
        st.write("No books available in the library.")


def borrow_book(book_id, srn):
    conn = connect_to_db()
    cursor = conn.cursor()
    date_borrowed = datetime.now()
    due_date = date_borrowed + timedelta(days=14)  # Assuming a 2-week borrowing period
    query = """
        UPDATE library_management 
        SET srn = %s, date_borrowed = %s, due_date = %s, return_date = NULL 
        WHERE book_id = %s AND srn IS NULL
    """
    cursor.execute(query, (srn, date_borrowed, due_date, book_id))
    conn.commit()
    if cursor.rowcount:
        print("Book borrowed successfully.")
    else:
        print("Book is already borrowed or not available.")
    cursor.close()
    conn.close()
    st.success("Book borrowed successfully.")

def return_book(book_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    return_date = datetime.now()

    # Calculate the penalty if overdue
    cursor.execute("SELECT due_date FROM library_management WHERE book_id = %s", (book_id,))
    due_date = cursor.fetchone()[0]
    overdue_days = (return_date - due_date).days
    penalty_amount = 0.00 if overdue_days <= 0 else overdue_days * 10  # Assuming $10 per overdue day

    query = """
        UPDATE library_management 
        SET return_date = %s, penalty_days = %s, penalty_amount = %s 
        WHERE book_id = %s
    """
    cursor.execute(query, (return_date, max(0, overdue_days), penalty_amount, book_id))
    conn.commit()
    st.success("Book returned successfully.")
    cursor.close()
    conn.close()

def check_penalty(srn):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT penalty_amount FROM library_management WHERE srn = %s AND return_date IS NULL"
    cursor.execute(query, (srn,))
    penalties = cursor.fetchall()
    total_penalty = sum([penalty[0] for penalty in penalties])
    print(f"Total penalty for SRN {srn}: ${total_penalty:.2f}")
    cursor.close()
    conn.close()

def get_books_borrowed_by_student(srn):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT book_id, book_title, author_name FROM library_management WHERE srn = %s AND return_date IS NULL"
    cursor.execute(query, (srn,))
    books = cursor.fetchall()
    for book in books:
        print(book)
    cursor.close()
    conn.close()

def list_overdue_books():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM library_management WHERE due_date < CURDATE() AND return_date IS NULL"
    cursor.execute(query)
    overdue_books = cursor.fetchall()
    for book in overdue_books:
        print(book)
    cursor.close()
    conn.close()

def search_book(search_term):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM library_management WHERE book_title LIKE %s OR author_name LIKE %s"
    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    for book in results:
        print(book)
    cursor.close()
    conn.close()

def list_available_books():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM library_management WHERE srn IS NULL"
    cursor.execute(query)
    available_books = cursor.fetchall()
    for book in available_books:
        print(book)
    cursor.close()
    conn.close()

def check_book_availability(book_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT srn FROM library_management WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    status = cursor.fetchone()
    if status[0] is None:
        print("Book is available for borrowing.")
    else:
        print("Book is currently borrowed.")
    cursor.close()
    conn.close()

def list_all_borrowed_books():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM library_management WHERE srn IS NOT NULL AND return_date IS NULL"
    cursor.execute(query)
    borrowed_books = cursor.fetchall()
    for book in borrowed_books:
        print(book)
    cursor.close()
    conn.close()

def calculate_total_penalty_for_student(srn):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT SUM(penalty_amount) FROM library_management WHERE srn = %s AND return_date IS NULL"
    cursor.execute(query, (srn,))
    total_penalty = cursor.fetchone()[0] or 0.00
    print(f"Total penalty for SRN {srn}: ${total_penalty:.2f}")
    cursor.close()
    conn.close()

def track_book_due_dates():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT book_id, book_title, due_date FROM library_management WHERE return_date IS NULL"
    cursor.execute(query)
    due_dates = cursor.fetchall()
    for book in due_dates:
        print(f"Book ID: {book[0]}, Title: {book[1]}, Due Date: {book[2]}")
    cursor.close()
    conn.close()



# Define functions (add_new_book, remove_book, etc. would be here)
# ...

# Streamlit app layout
st.title("Library Management System")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select Functionality",
    [
        "Add New Book",
        "Remove Book",
        "Update Book Info",
        "List All Books",
        "Borrow Book",
        "Return Book",
        "Check Penalty",
        "Get Books Borrowed by Student",
        "List Overdue Books",
        "Search Book",
        "List Available Books",
        "Check Book Availability",
        "List All Borrowed Books",
        "Calculate Total Penalty for Student",
        "Track Book Due Dates"
    ]
)

# Functions as per selected option in the sidebar
if menu == "Add New Book":
    st.header("Add New Book")
    book_title = st.text_input("Book Title")
    author_name = st.text_input("Author Name")
    if st.button("Add Book"):
        add_new_book(book_title, author_name)

elif menu == "Remove Book":
    st.header("Remove Book")
    book_id = st.number_input("Book ID", min_value=1)
    if st.button("Remove Book"):
        remove_book(book_id)

elif menu == "Update Book Info":
    st.header("Update Book Info")
    book_id = st.number_input("Book ID", min_value=1)
    book_title = st.text_input("New Book Title (Leave blank to keep unchanged)")
    author_name = st.text_input("New Author Name (Leave blank to keep unchanged)")
    if st.button("Update Book"):
        update_book_info(book_id, book_title, author_name)

elif menu == "List All Books":
    st.header("List All Books")
    if st.button("Show Books"):
        list_all_books()

elif menu == "Borrow Book":
    st.header("Borrow Book")
    book_id = st.number_input("Book ID", min_value=1)
    srn = st.text_input("Student SRN")
    if st.button("Borrow Book"):
        borrow_book(book_id, srn)

elif menu == "Return Book":
    st.header("Return Book")
    book_id = st.number_input("Book ID", min_value=1)
    if st.button("Return Book"):
        return_book(book_id)

elif menu == "Check Penalty":
    st.header("Check Penalty")
    srn = st.text_input("Student SRN")
    if st.button("Check Penalty"):
        check_penalty(srn)

elif menu == "Get Books Borrowed by Student":
    st.header("Books Borrowed by Student")
    srn = st.text_input("Student SRN")
    if st.button("Get Borrowed Books"):
        get_books_borrowed_by_student(srn)

elif menu == "List Overdue Books":
    st.header("Overdue Books")
    if st.button("Show Overdue Books"):
        list_overdue_books()

elif menu == "Search Book":
    st.header("Search Book")
    search_term = st.text_input("Enter book title or author name")
    if st.button("Search"):
        search_book(search_term)

elif menu == "List Available Books":
    st.header("Available Books")
    if st.button("Show Available Books"):
        list_available_books()

elif menu == "Check Book Availability":
    st.header("Check Book Availability")
    book_id = st.number_input("Book ID", min_value=1)
    if st.button("Check Availability"):
        check_book_availability(book_id)

elif menu == "List All Borrowed Books":
    st.header("Borrowed Books")
    if st.button("Show Borrowed Books"):
        list_all_borrowed_books()

elif menu == "Calculate Total Penalty for Student":
    st.header("Total Penalty for Student")
    srn = st.text_input("Student SRN")
    if st.button("Calculate Penalty"):
        calculate_total_penalty_for_student(srn)

elif menu == "Track Book Due Dates":
    st.header("Track Book Due Dates")
    if st.button("Show Due Dates"):
        track_book_due_dates()
