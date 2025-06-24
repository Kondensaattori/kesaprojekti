
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
def init_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("konstan-kesaprojekti-293f86ea4fd1.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("School Communication App").sheet1
    return sheet

# Simulated user database
users = {
    "alice": "Teacher",
    "bob": "Deputy",
    "carol": "Assigned Teacher",
    "dave": "Principal"
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

st.title("🏫 School Communication App")

if not st.session_state.logged_in:
    username = st.text_input("Enter your username")
    if st.button("Login"):
        if username in users:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]
            st.success(f"Logged in as {username} ({st.session_state.role})")
        else:
            st.error("Invalid username")
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    role = st.session_state.role
    sheet = init_gsheet()

    if role == "Teacher":
        st.subheader("Report Absence")
        if st.button("Report Absence"):
            sheet.append_row(["Absence", st.session_state.username])
            st.success("Absence reported. Principal and assigned teacher will be notified.")

    elif role == "Deputy":
        st.subheader("Register Availability")
        if st.button("Register Availability"):
            sheet.append_row(["Available", st.session_state.username])
            st.success("Availability registered.")

    elif role == "Assigned Teacher":
        st.subheader("View Absences")
        absences = sheet.findall("Absence")
        absent_names = [sheet.cell(cell.row, 2).value for cell in absences]
        st.write("Absent Teachers:")
        st.write(absent_names if absent_names else "No absences reported.")

        st.subheader("View Available Deputies")
        deputies = sheet.findall("Available")
        deputy_names = [sheet.cell(cell.row, 2).value for cell in deputies]
        st.write("Available Deputies:")
        st.write(deputy_names if deputy_names else "No deputies available.")

    elif role == "Principal":
        st.subheader("Absence Log")
        absences = sheet.findall("Absence")
        absent_names = [sheet.cell(cell.row, 2).value for cell in absences]
        st.write("Reported Absences:")
        st.write(absent_names if absent_names else "No absences reported.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.experimental_rerun()
