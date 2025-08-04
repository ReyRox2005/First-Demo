#my first app
import streamlit as st
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText

# ---- Session Init ----
for key in ['logged_in', 'user_email', 'generated_otp', 'email_temp', 'password_temp', 'mode']:
    if key not in st.session_state:
        st.session_state[key] = False if key == 'logged_in' else '' if 'email' in key else None if 'otp' in key else 'login'

# ---- DB Connection ----
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="app",
    )

# ---- Helpers ----
def is_valid_college_email(email):
    return email.endswith("@spsu.ac.in")

def register_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

def user_exists(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def update_password(email, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=%s WHERE email=%s", (new_password, email))
    conn.commit()
    cursor.close()
    conn.close()

def send_otp_email(receiver_email, otp):
    sender_email = "spsu.me22@gmail.com"
    sender_password = "oicd ftof itgt ldtr"
    message = MIMEText(f"Your OTP is: {otp}")
    message['Subject'] = "Your OTP"
    message['From'] = sender_email
    message['To'] = receiver_email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")

# ---- Homepage UI ----
def show_homepage():
    st.set_page_config(page_title="CampusVibe", layout="wide")
    st.markdown("""
        <style>
            .block-container { padding: 1rem 2rem; }
            .note-card {
                background-color: #f4f0ff;
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 1rem;
                box-shadow: 0 0 5px #ccc;
            }
            .note-title { font-weight: 600; }
            .chat-box {
                background-color: #f0f4ff;
                padding: 1rem;
                border-radius: 10px;
            }
            .ask-box {
                background-color: #fdf4ff;
                padding: 1rem;
                border-radius: 10px;
            }
            .submit-button {
                background-color: #6557f5;
                color: white;
                padding: 0.4rem 1.2rem;
                border-radius: 5px;
                margin: 0.5rem 0;
                border: none;
            }
            .accept-button {
                background-color: #30c05b;
                color: white;
                border-radius: 5px;
                padding: 0.3rem 0.8rem;
                border: none;
            }
            .reject-button {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 0.3rem 0.8rem;
                border: none;
            }
        </style>
    """, unsafe_allow_html=True)

    col_logo, col_search, col_notify = st.columns([2, 6, 1])
    col_logo.markdown("### 🎓 CampusVibe")
    col_search.text_input("Search anything...", label_visibility="collapsed", placeholder="Search...")
    col_notify.markdown("🔔", unsafe_allow_html=True)
    st.markdown("---")

    with st.sidebar:
        st.markdown("### 🎯 Filters")
        st.selectbox("Select Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        st.selectbox("Branch", ["CSE", "ECE", "ME", "CE"])
        st.selectbox("Subject", ["DSA", "OS", "DBMS", "CN", "AI"])
        st.markdown("<button class='submit-button'>Upload Notes 🧑‍🏫</button>", unsafe_allow_html=True)
        st.markdown("<button class='submit-button' style='background-color:#28a745;'>Chat with Senior💬</button>", unsafe_allow_html=True)

    st.markdown("## 🔥 Trending Notes")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""<div class='note-card'><div class='note-title'>📄 DSA Unit 1</div>
            ⭐ 32 downloads<br><br>
            <button class='submit-button'>View</button>
            <button class='submit-button'>Download</button></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class='note-card'><div class='note-title'>📄 OS Unit 2</div>
            ⭐ 42 downloads<br><br>
            <button class='submit-button'>View</button>
            <button class='submit-button'>Download</button></div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div class='note-card'><div class='note-title'>📄 DBMS Unit 3</div>
            ⭐ 52 downloads<br><br>
            <button class='submit-button'>View</button>
            <button class='submit-button'>Download</button></div>""", unsafe_allow_html=True)

    st.markdown("""<div class='chat-box'>
        <h4>💬 Chat Requests</h4>
        <p><i>"anonFirstYr23" wants to connect. Topic: DSA</i></p>
        <button class='accept-button'>Accept</button>
        <button class='reject-button'>Reject</button>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class='ask-box'>
        <h4>🧠 Ask a Senior</h4>
        <p><i>"What to study for placement in 2nd year?"</i></p>
        <button class='submit-button'>Answer Question</button>
    </div>""", unsafe_allow_html=True)

    st.markdown("### Ask Your Question")
    st.text_area("Type your question here...")

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ---- Main Logic ----
if st.session_state.logged_in:
    show_homepage()
else:
    st.title("CampusVibe Login System")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Login"):
            st.session_state.mode = 'login'
            st.session_state.generated_otp = None
    with col2:
        if st.button("Register"):
            st.session_state.mode = 'register'
            st.session_state.generated_otp = None
    with col3:
        if st.button("Forgot Password"):
            st.session_state.mode = 'forgot'
            st.session_state.generated_otp = None

    if st.session_state.mode == 'login':
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Send OTP for Login"):
            if not is_valid_college_email(email):
                st.error("Only college emails allowed.")
            elif login_user(email, password):
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                st.session_state.email_temp = email
                st.session_state.password_temp = password
                send_otp_email(email, otp)
                st.success("OTP sent to your email.")
            else:
                st.error("Invalid credentials.")

        if st.session_state.generated_otp:
            otp_input = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                if otp_input == st.session_state.generated_otp:
                    st.session_state.logged_in = True
                    st.session_state.user_email = st.session_state.email_temp
                    st.rerun()
                else:
                    st.error("Invalid OTP. Try again.")

    elif st.session_state.mode == 'register':
        st.subheader("Register")
        email = st.text_input("College Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register Now"):
            if not is_valid_college_email(email):
                st.error("Only college emails allowed.")
            elif register_user(email, password):
                st.success("Registered successfully.")
            else:
                st.warning("Email already registered.")

    elif st.session_state.mode == 'forgot':
        st.subheader("Forgot Password")
        email = st.text_input("Registered Email", key="fp_email")
        if st.button("Send OTP for Reset"):
            if not is_valid_college_email(email):
                st.error("Only college emails allowed.")
            elif not user_exists(email):
                st.warning("User not found.")
            else:
                otp = str(random.randint(100000, 999999))
                st.session_state.generated_otp = otp
                st.session_state.email_temp = email
                send_otp_email(email, otp)
                st.success("OTP sent to your email.")

        if st.session_state.generated_otp:
            otp_input = st.text_input("Enter OTP")
            new_password = st.text_input("New Password", type="password")
            if st.button("Reset Password"):
                if otp_input == st.session_state.generated_otp:
                    update_password(st.session_state.email_temp, new_password)
                    st.success("Password updated successfully.")
                    st.session_state.generated_otp = None
                else:
                    st.error("Invalid OTP")
