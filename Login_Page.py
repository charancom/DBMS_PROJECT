import bcrypt
import mysql.connector
import streamlit as st


# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Hello@123",
        database="StudentManagement"
    )

# Retrieve stored user credentials
def get_user_credentials(username):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT username, hashed_password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user


# Verify password using bcrypt
def verify_password(input_password, stored_password_hash):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password_hash.encode('utf-8'))


# Display login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_credentials(username)
        if user and verify_password(password, user['hashed_password']):
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid username or password")


# Function to display content of different systems (UI for each module)
def show_system(system_choice):
    if system_choice == "Attendance System":
        st.title("Attendance System")
        st.write("This is the Attendance System functionality.")  # Replace with actual app code
    elif system_choice == "Grading":
        st.title("Grading System")
        st.write("This is the Grading System functionality.")  # Replace with actual app code
    elif system_choice == "Library Management":
        st.title("Library Management System")
        st.write("This is the Library Management System functionality.")  # Replace with actual app code
    elif system_choice == "Payments":
        st.title("Payments System")
        st.write("This is the Payments System functionality.")  # Replace with actual app code
    elif system_choice == "Personal Details":
        st.title("Personal Details System")
        st.write("This is the Personal Details System functionality.")  # Replace with actual app code
    elif system_choice == "Re-Addressal System":
        st.title("Re-Addressal System")
        st.write("This is the Re-Addressal System functionality.")  # Replace with actual app code


# Main application
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    st.write(f"Welcome, {st.session_state['username']}!")

    # Menu for selecting which system to access
    system_choice = st.selectbox("Select a system to access:", [
        "Attendance System", "Grading", "Library Management", "Payments", "Personal Details", "Re-Addressal System"
    ])

    if st.button("Open Selected System"):
        show_system(system_choice)
