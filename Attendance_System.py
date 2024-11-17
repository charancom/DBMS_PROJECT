# import mysql.connector
# import datetime
# def connect_to_db():
#     return mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",
#         password="Hello@123",
#         database="StudentManagement"
#     )
#
# def view_attendance(semester, srn):
#     table_name = f"sem_{semester}_attendance"
#     conn = connect_to_db()
#     cursor = conn.cursor()
#
#     query = f"""
#         SELECT subject_1_attendance, subject_2_attendance,
#                subject_3_attendance, subject_4_attendance, subject_5_attendance
#         FROM {table_name} WHERE srn = %s
#     """
#     cursor.execute(query, (srn,))
#     result = cursor.fetchone()
#
#     cursor.close()
#     conn.close()
#
#     if result:
#         attendance = {
#             "Subject 1": result[0],
#             "Subject 2": result[1],
#             "Subject 3": result[2],
#             "Subject 4": result[3],
#             "Subject 5": result[4]
#         }
#         print(f"Attendance for SRN {srn} in Semester {semester}:")
#         for subject, percentage in attendance.items():
#             print(f"{subject}: {percentage}%")
#     else:
#         print(f"No attendance record found for SRN {srn} in Semester {semester}.")
#
#
# def check_minimum_attendance(semester, srn, min_attendance=75.0):
#     table_name = f"sem_{semester}_attendance"
#     conn = connect_to_db()
#     cursor = conn.cursor()
#
#     query = f"""
#         SELECT subject_1_attendance, subject_2_attendance,
#                subject_3_attendance, subject_4_attendance, subject_5_attendance
#         FROM {table_name} WHERE srn = %s
#     """
#     cursor.execute(query, (srn,))
#     result = cursor.fetchone()
#
#     cursor.close()
#     conn.close()
#
#     if result:
#         meets_requirement = all(att >= min_attendance for att in result)
#         if meets_requirement:
#             print(f"SRN {srn} meets the minimum attendance requirement for all subjects in Semester {semester}.")
#         else:
#             print(
#                 f"SRN {srn} does NOT meet the minimum attendance requirement for all subjects in Semester {semester}.")
#             for i, att in enumerate(result, start=1):
#                 if att < min_attendance:
#                     print(f"Subject {i}: {att}% (Below {min_attendance}%)")
#     else:
#         print(f"No attendance record found for SRN {srn} in Semester {semester}.")


import streamlit as st
import mysql.connector


# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Hello@123",
        database="StudentManagement"
    )


# Display attendance for a specific SRN and semester
def view_attendance(semester, srn):
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
        SELECT subject_1_attendance, subject_2_attendance, 
               subject_3_attendance, subject_4_attendance, subject_5_attendance
        FROM attendance WHERE semester = %s AND srn = %s
    """
    cursor.execute(query, (semester, srn))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        attendance = {
            "Subject 1": result[0],
            "Subject 2": result[1],
            "Subject 3": result[2],
            "Subject 4": result[3],
            "Subject 5": result[4]
        }
        st.subheader(f"Attendance for SRN {srn} in Semester {semester}")
        for subject, percentage in attendance.items():
            st.write(f"{subject}: {percentage}%")
    else:
        st.warning(f"No attendance record found for SRN {srn} in Semester {semester}.")


# Check if the attendance meets a minimum threshold
def check_minimum_attendance(semester, srn, min_attendance=75.0):
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
        SELECT subject_1_attendance, subject_2_attendance, 
               subject_3_attendance, subject_4_attendance, subject_5_attendance
        FROM attendance WHERE semester = %s AND srn = %s
    """
    cursor.execute(query, (semester, srn))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        meets_requirement = all(att >= min_attendance for att in result)
        if meets_requirement:
            st.success(f"SRN {srn} meets the minimum attendance requirement for all subjects in Semester {semester}.")
        else:
            st.error(
                f"SRN {srn} does NOT meet the minimum attendance requirement for all subjects in Semester {semester}.")
            for i, att in enumerate(result, start=1):
                if att < min_attendance:
                    st.write(f"Subject {i}: {att}% (Below {min_attendance}%)")
    else:
        st.warning(f"No attendance record found for SRN {srn} in Semester {semester}.")


# Streamlit main menu for attendance functions
def main_menu():
    st.sidebar.title("Attendance Management System")
    option = st.sidebar.selectbox("Choose an option:",
                                  ["View Attendance", "Check Minimum Attendance"])

    if option == "View Attendance":
        st.title("View Attendance")
        semester = st.text_input("Enter Semester:")
        srn = st.text_input("Enter SRN:")

        if st.button("View Attendance"):
            view_attendance(semester, srn)

    elif option == "Check Minimum Attendance":
        st.title("Check Minimum Attendance")
        semester = st.text_input("Enter Semester:")
        srn = st.text_input("Enter SRN:")
        min_attendance = st.number_input("Minimum Attendance Requirement (%)", min_value=0.0, max_value=100.0,
                                         value=75.0)

        if st.button("Check Attendance"):
            check_minimum_attendance(semester, srn, min_attendance)


if __name__ == "__main__":
    main_menu()
