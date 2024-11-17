import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root1',
        passwd='Hello@1234',
        database='StudentManagement'
    )

# Function to view payment details by SRN
def view_payment_details(srn):
    conn = connect_to_db()
    cursor = conn.cursor()
    select_query = "SELECT * FROM student_payment WHERE srn = %s"
    try:
        cursor.execute(select_query, (srn,))
        results = cursor.fetchall()
        if results:
            st.write("Payment Details for SRN:", srn)
            payment_df = pd.DataFrame(results, columns=["Payment ID", "Academic Year", "Branch", "Payment Type", "Demand Amount", "Paid Amount", "Balance Due", "Due Date", "Number of Transactions", "Status", "SRN"])
            st.dataframe(payment_df)
        else:
            st.write("No payment records found for the specified SRN.")
    except Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to update payment status by Payment ID
def update_payment_status(payment_id, new_status):
    conn = connect_to_db()
    cursor = conn.cursor()
    update_query = "UPDATE student_payment SET status = %s WHERE payment_id = %s"
    try:
        cursor.execute(update_query, (new_status, payment_id))
        conn.commit()
        st.success(f"Payment status updated to '{new_status}' for Payment ID: {payment_id}")
    except Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to insert a new payment entry
def insert_student_payment(academic_year, branch, payment_type, demand_amount, paid_amount, balance_due, due_date, number_of_txn, status, srn):
    conn = connect_to_db()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO student_payment 
    (academic_year, branch, payment_type, demand_amount, paid_amount, balance_due, due_date, number_of_txn, status, srn)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(insert_query, (academic_year, branch, payment_type, demand_amount, paid_amount, balance_due, due_date, number_of_txn, status, srn))
        conn.commit()
        st.success(f"Payment record inserted for SRN: {srn}")
    except Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to find SRNs with no payment or outstanding balance
def find_srn_without_payment_or_balance():
    conn = connect_to_db()
    cursor = conn.cursor()
    select_query = """
    SELECT pd.srn 
    FROM personal_details pd
    LEFT JOIN student_payment sp ON pd.srn = sp.srn
    WHERE sp.srn IS NULL OR sp.balance_due <> 0
    """
    try:
        cursor.execute(select_query)
        results = cursor.fetchall()
        if results:
            st.write("SRNs without payments or with outstanding balances:")
            srn_df = pd.DataFrame(results, columns=["SRN"])
            st.dataframe(srn_df)
        else:
            st.write("All SRNs have completed payments with a balance due of 0.")
    except Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Streamlit UI Layout
st.title("Student Payment Management System")

# Selection of actions
action = st.selectbox("Select an Action", ["View Payment Details", "Update Payment Status", "Insert Payment Record", "Find SRNs Without Payment or Outstanding Balance"])

if action == "View Payment Details":
    srn = st.text_input("Enter SRN to View Payment Details:")
    if st.button("View Payment"):
        view_payment_details(srn)

elif action == "Update Payment Status":
    payment_id = st.number_input("Enter Payment ID:", min_value=1, step=1)
    new_status = st.selectbox("Select New Status", ["Paid", "Pending", "Overdue"])
    if st.button("Update Status"):
        update_payment_status(payment_id, new_status)

elif action == "Insert Payment Record":
    with st.form("Insert Payment Form"):
        academic_year = st.text_input("Academic Year:")
        branch = st.text_input("Branch:")
        payment_type = st.selectbox("Payment Type", ["Tuition", "Hostel", "Exam"])
        demand_amount = st.number_input("Demand Amount:", min_value=0.0, step=0.01)
        paid_amount = st.number_input("Paid Amount:", min_value=0.0, step=0.01)
        balance_due = demand_amount - paid_amount
        due_date = st.date_input("Due Date")
        number_of_txn = st.number_input("Number of Transactions:", min_value=0, step=1)
        status = st.selectbox("Status", ["Paid", "Pending", "Overdue"])
        srn = st.text_input("SRN:")

        if st.form_submit_button("Insert Payment"):
            insert_student_payment(academic_year, branch, payment_type, demand_amount, paid_amount, balance_due, due_date, number_of_txn, status, srn)

elif action == "Find SRNs Without Payment or Outstanding Balance":
    if st.button("Find SRNs"):
        find_srn_without_payment_or_balance()
