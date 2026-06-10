import streamlit as st
import sys
import os

# Path Setup
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from utils.auth import init_connection, login_user, signup_user

st.set_page_config(page_title="Property Operations Tracker", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'supabase_client' not in st.session_state:
    st.session_state['supabase_client'] = init_connection()

def main():
    # --- AUTHENTICATED SIDEBAR ---
    if st.session_state['authenticated']:
        with st.sidebar:
            st.title("Navigation")
            # This is the new "User Profile" area
            with st.expander("👤 User Profile"):
                st.write(f"**Email:** {st.session_state.get('user_email', 'N/A')}")
                if st.button("Update Password"):
                    st.info("Password update logic triggered.") # Placeholder
            
            st.divider()
            # Navigation links remain here
            if st.button("Log Out"):
                st.session_state['authenticated'] = False
                st.rerun()

    # --- LOGIN / SIGNUP VIEW ---
    if not st.session_state['authenticated']:
        st.title("Secure Portal Login")
        tab1, tab2 = st.tabs(["Log In", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Log In"):
                    user, role = login_user(email, password)
                    if user:
                        st.session_state['authenticated'] = True
                        st.session_state['user_role'] = role
                        st.session_state['user_email'] = email
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
        with tab2:
            st.markdown("### Register New Account")
            with st.form("signup_form"):
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                admin_code = st.text_input("Executive Invite Code", type="password")
                if st.form_submit_button("Create Account"):
                    role = 'executive' if admin_code == "PORTFOLIO2026" else 'manager'
                    user, assigned_role = signup_user(new_email, new_password, role)
                    if user:
                        st.success("Account created!")
    
    # --- AUTHENTICATED MAIN AREA ---
    else:
        st.title("Dashboard Overview")
        st.write("Welcome to the Property Operations Tracker.")

if __name__ == "__main__":
    main()
