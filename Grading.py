import streamlit as st
import mysql.connector
import pandas as pd
from decimal import Decimal


# Connect to the database
def connect_to_db():
    return mysql.connector.connect(host='127.0.0.1', user='root', passwd='Hello@123', database='StudentManagement')


# Function to insert data into subject_grades table
def insert_data(cursor, subject_id, srn, subject_name, grade, current_semester, subject_credit):
    insert_query = """
    INSERT INTO subject_grades (subject_id, srn, subject_name, grade, current_semester, subject_credit)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (subject_id, srn, subject_name, grade, current_semester, subject_credit))


# Function to view all data in subject_grades
def view_data(cursor):
    select_query = "SELECT * FROM subject_grades"
    cursor.execute(select_query)
    return cursor.fetchall()


# Function to calculate SGPA
def calculate_sgpa_with_total_credits(cursor):
    select_query = """
        SELECT srn, current_semester, 
               SUM(subject_credit * grade_point) AS total_points, 
               SUM(subject_credit) AS total_credits
        FROM (
            SELECT srn, current_semester, subject_credit, 
                CASE grade
                    WHEN 'S' THEN 10
                    WHEN 'A' THEN 9
                    WHEN 'B' THEN 8
                    WHEN 'C' THEN 7
                    WHEN 'D' THEN 6
                    WHEN 'E' THEN 5
                    WHEN 'F' THEN 0
                    ELSE NULL
                END AS grade_point
            FROM subject_grades
        ) AS graded_subjects
        GROUP BY srn, current_semester
    """
    cursor.execute(select_query)
    return cursor.fetchall()


# Function to calculate CGPA
def calculate_cgpa(cursor, srn):
    data = calculate_sgpa_with_total_credits(cursor)
    total_points = Decimal('0')
    total_credits = Decimal('0')

    for row in data:
        if row[0] == srn:  # Match specific SRN
            total_points += row[2]
            total_credits += row[3]

    if total_credits > 0:
        return total_points / total_credits
    else:
        return None


# Streamlit UI
def main():
    st.sidebar.title("Student Management System")
    conn = connect_to_db()
    cursor = conn.cursor()

    # Menu options
    option = st.sidebar.selectbox("Select an operation:", [
        "Insert Subject Grade", "View All Grades", "Calculate SGPA", "Calculate CGPA", "Assign Scholarships"
    ])

    # Insert subject grade
    if option == "Insert Subject Grade":
        st.header("Insert Subject Grade")
        subject_id = st.text_input("Subject ID")
        srn = st.text_input("SRN")
        subject_name = st.text_input("Subject Name")
        grade = st.selectbox("Grade", ["S", "A", "B", "C", "D", "E", "F"])
        current_semester = st.number_input("Current Semester", min_value=1, max_value=10)
        subject_credit = st.number_input("Subject Credit", min_value=1.0)

        if st.button("Insert Grade"):
            try:
                insert_data(cursor, subject_id, srn, subject_name, grade, current_semester, subject_credit)
                conn.commit()
                st.success("Data inserted successfully.")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")

    # View all grades
    elif option == "View All Grades":
        st.header("View All Grades")
        try:
            data = view_data(cursor)
            df = pd.DataFrame(data, columns=["Subject ID", "SRN", "Subject Name", "Grade", "Semester", "Credits"])
            st.dataframe(df)
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

    # Calculate SGPA for each student
    elif option == "Calculate SGPA":
        st.header("Calculate SGPA")
        try:
            sgpa_data = calculate_sgpa_with_total_credits(cursor)
            sgpa_df = pd.DataFrame(sgpa_data, columns=["SRN", "Semester", "Total Points", "Total Credits"])
            sgpa_df["SGPA"] = sgpa_df["Total Points"] / sgpa_df["Total Credits"]
            st.dataframe(sgpa_df[["SRN", "Semester", "SGPA"]])
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

    # Calculate CGPA
    elif option == "Calculate CGPA":
        st.header("Calculate CGPA")
        srn = st.text_input("Enter SRN for CGPA calculation")

        if st.button("Calculate CGPA"):
            try:
                cgpa = calculate_cgpa(cursor, srn)
                if cgpa:
                    st.success(f"CGPA for {srn} is: {cgpa:.2f}")
                else:
                    st.warning("No data available to calculate CGPA.")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")

    # Assign scholarships based on CGPA
    elif option == "Assign Scholarships":
        st.header("Scholarship Eligibility")
        try:
            select_query = "SELECT srn, cgpa FROM student_results WHERE cgpa > 3.0"
            cursor.execute(select_query)
            eligible_students = cursor.fetchall()
            if eligible_students:
                for student in eligible_students:
                    st.write(f"Student {student[0]} with CGPA {student[1]} is awarded a scholarship.")
            else:
                st.info("No students eligible for scholarships.")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()