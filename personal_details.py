import streamlit as st
import mysql.connector
import pandas as pd

# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Hello@123",
        database="StudentManagement"
    )

# Functions from your code (same as you provided above)
#
# # 1. Add New Student
def add_student(name, srn, prn, branch, section, semester, contact_no, qualifying_exam_rank, address, program, father_name, mother_name, father_phone_no, mother_phone_no):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        INSERT INTO personal_details (name, srn, prn, branch, section, semester, contact_no, qualifying_exam_rank, address, program, father_name, mother_name, father_phone_no, mother_phone_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, srn, prn, branch, section, semester, contact_no, qualifying_exam_rank, address, program, father_name, mother_name, father_phone_no, mother_phone_no))
    db.commit()
    cursor.close()
    db.close()

# 2. Update Student Information

# 3. Delete Student Record
def delete_student(srn):
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM personal_details WHERE srn = %s"
    cursor.execute(query, (srn,))
    db.commit()
    cursor.close()
    db.close()

# 4. Retrieve Student Information by SRN
def get_student_by_srn(srn):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM personal_details WHERE srn = %s"
    cursor.execute(query, (srn,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result

# 5. List All Students in a Specific Branch or Section
def list_students_by_branch_section(branch, section):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM personal_details WHERE branch = %s AND section = %s"
    cursor.execute(query, (branch, section))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

# 6. Filter Students by Semester
def filter_students_by_semester(semester):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM personal_details WHERE semester = %s"
    cursor.execute(query, (semester,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

# 7. Update Student Contact Information
# Function to update student contact information
def update_contact_info(srn, contact_no=None, father_phone_no=None, mother_phone_no=None):
    fields = {}
    if contact_no:
        fields["contact_no"] = contact_no
    if father_phone_no:
        fields["father_phone_no"] = father_phone_no
    if mother_phone_no:
        fields["mother_phone_no"] = mother_phone_no

    # Only call update_student if there are fields to update
    if fields:
        update_student(srn, **fields)

# Function to update student details in the database
def update_student(srn, **fields):
    db = connect_to_db()
    cursor = db.cursor()

    if not fields:
        return  # Nothing to update

    # Construct the SET clause for the SQL query
    set_clause = ", ".join(f"{key} = %s" for key in fields.keys())
    query = f"UPDATE personal_details SET {set_clause} WHERE srn = %s"

    try:
        # Execute the query with the field values and the SRN
        cursor.execute(query, tuple(fields.values()) + (srn,))
        db.commit()  # Commit the changes
    except Exception as e:
        print("An error occurred while updating student:", e)
        st.error("Failed to update student information.")
    finally:
        cursor.close()
        db.close()

# 9. Count Students in a Particular Program
def count_students_by_program(program):
    db = connect_to_db()
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM personal_details WHERE program = %s"
    cursor.execute(query, (program,))
    result = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return result

# 10. Search Student by Name
def search_student_by_name(name):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM personal_details WHERE name LIKE %s"
    cursor.execute(query, ("%" + name + "%",))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

# 11. List All Students Missing Contact Information
def list_students_missing_contact_info():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT * FROM personal_details
        WHERE contact_no IS NULL OR father_contact IS NULL OR mother_contact IS NULL
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

# 12. Get All Student SRNs
def get_all_student_srns():
    db = connect_to_db()
    cursor = db.cursor()
    query = "SELECT srn FROM personal_details"
    cursor.execute(query)
    srns = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()
    return srns

# 13. Find Students by Address
def find_students_by_address(address):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM personal_details WHERE address LIKE %s"
    cursor.execute(query, ("%" + address + "%",))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

# 14. Get Total Students Count
def get_total_student_count():
    db = connect_to_db()
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM personal_details"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return result


# Streamlit UI
st.title("Student Management System")

menu = [
    "Add New Student",
    "Update Student Information",
    "Delete Student Record",
    "Retrieve Student Information by SRN",
    "List Students by Branch and Section",
    "Filter Students by Semester",
    "Update Student Contact Information",
    "Count Students by Program",
    "Search Student by Name",
    "Get All Student SRNs",
    "Get Total Student Count"
]

choice = st.sidebar.selectbox("Choose an Option", menu)

# Option 1: Add New Student
if choice == "Add New Student":
    st.subheader("Add New Student")
    # Fields for user input
    name = st.text_input("Name")
    srn = st.text_input("SRN")
    prn = st.text_input("PRN")
    branch = st.text_input("Branch")
    section = st.text_input("Section")
    semester = st.number_input("Semester", min_value=1, max_value=8)
    contact_no = st.text_input("Contact Number")
    qualifying_exam_rank = st.number_input("Qualifying Exam Rank", min_value=0)
    address = st.text_input("Address")
    program = st.text_input("Program")
    father_name = st.text_input("Father's Name")
    mother_name = st.text_input("Mother's Name")
    father_contact = st.text_input("Father's Contact Number")
    mother_contact = st.text_input("Mother's Contact Number")

    if st.button("Add Student"):
        add_student(name, srn, prn, branch, section, semester, contact_no, qualifying_exam_rank, address, program, father_name, mother_name, father_contact, mother_contact)
        st.success("Student added successfully")

# Option 2: Update Student Information
elif choice == "Update Student Information":
    st.subheader("Update Student Information")
    srn = st.text_input("Enter SRN of student to update")
    fields = {}
    # User inputs for each field they might want to update
    if st.text_input("Name (leave blank if no change)"):
        fields["name"] = st.text_input("Name")
    if st.text_input("Contact Number"):
        fields["contact_no"] = st.text_input("Contact Number")
    # Add more fields as necessary
    if fields and st.button("Update Student"):
        update_student(srn, **fields)
        st.success("Student information updated")

# Option 3: Delete Student Record
elif choice == "Delete Student Record":
    st.subheader("Delete Student Record")
    srn = st.text_input("Enter SRN of student to delete")
    if st.button("Delete Student"):
        delete_student(srn)
        st.success("Student record deleted")

# Option 4: Retrieve Student Information by SRN
elif choice == "Retrieve Student Information by SRN":
    st.subheader("Retrieve Student Information by SRN")
    srn = st.text_input("Enter SRN")
    if st.button("Retrieve"):
        student = get_student_by_srn(srn)
        if student:
            # Assuming 'student' is a dictionary, we convert it to a DataFrame for tabular display
            student_df = pd.DataFrame([student])  # Convert to DataFrame with one row
            st.table(student_df)  # Display as a table
        else:
            st.error("Student not found")

# Option 5: List Students by Branch and Section
elif choice == "List Students by Branch and Section":
    st.subheader("List Students by Branch and Section")
    branch = st.text_input("Branch")
    section = st.text_input("Section")
    if st.button("List Students"):
        students = list_students_by_branch_section(branch, section)
        if students:
            students_df = pd.DataFrame(students)  # Convert results to DataFrame
            st.table(students_df)  # Display as a table
        else:
            st.error("No students found for this branch and section")

# Option 6: Filter Students by Semester
elif choice == "Filter Students by Semester":
    st.subheader("Filter Students by Semester")
    semester = st.number_input("Semester", min_value=1, max_value=8)
    if st.button("Filter"):
        students = filter_students_by_semester(semester)
        if students:
            students_df = pd.DataFrame(students)  # Convert results to DataFrame
            st.table(students_df)  # Display as a table
        else:
            st.error("No students found for this semester")


# Option 7: Update Student Contact Information
elif choice == "Update Student Contact Information":
    st.subheader("Update Student Contact Information")
    srn = st.text_input("Enter SRN")
    contact_no = st.text_input("Contact Number (leave blank if no change)")
    father_phone_no = st.text_input("Father's Contact (leave blank if no change)")
    mother_phone_no = st.text_input("Mother's Contact (leave blank if no change)")

    if st.button("Update Contact Info"):
        update_contact_info(
            srn,
            contact_no=contact_no if contact_no else None,
            father_phone_no=father_phone_no if father_phone_no else None,
            mother_phone_no=mother_phone_no if mother_phone_no else None
        )
        st.success("Contact information updated successfully.")




# Example for Count Students by Program
elif choice == "Count Students by Program":
    st.subheader("Count Students by Program")
    program = st.text_input("Program")
    if st.button("Count"):
        count = count_students_by_program(program)
        st.write(f"Total students in program {program}: {count}")

# Example for Get Total Student Count
elif choice == "Get Total Student Count":
    st.subheader("Get Total Student Count")
    if st.button("Get Count"):
        total_count = get_total_student_count()
        st.write(f"Total number of students: {total_count}")

# Option 9: Search Student by Name
elif choice == "Search Student by Name":
    st.subheader("Search Student by Name")
    name = st.text_input("Enter name or part of the name to search")

    if st.button("Search"):
        results = search_student_by_name(name)

        # Check if results were found
        if results:
            # Convert results to a DataFrame for easier display
            results_df = pd.DataFrame(results)
            st.table(results_df)  # Display results as a table
        else:
            st.error("No students found with that name")


elif choice == "Get All Student SRNs":
    st.subheader("Get All Student SRNs")
    if st.button("Get SRNs"):
        srns = get_all_student_srns()
        if srns:
            st.write("List of Student SRNs:")
            srn_df = pd.DataFrame(srns, columns=["SRN"])  # Convert to DataFrame for better display
            st.table(srn_df)  # Display as a table
        else:
            st.error("No students found")

# Repeat this structure for other functions as necessary
