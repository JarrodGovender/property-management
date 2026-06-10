import streamlit as st
import sys
import os

# --- PATH SETUP ---
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from utils.auth import init_connection, login_user, signup_user

# --- CONFIGURATION ---
st.set_page_config(page_title="Property Operations Tracker", layout="wide")

# --- SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None
if 'supabase_client' not in st.session_state:
    st.session_state['supabase_client'] = init_connection()

# --- CSS HELPER ---
def hide_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- MAIN LOGIC ---
def main():
    if not st.session_state['authenticated']:
        hide_sidebar()
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
                        st.success("Account created! Please switch to the Log In tab.")
    
    else:
        # --- AUTHENTICATED SIDEBAR ---
        with st.sidebar:
            st.title("Navigation")
            with st.expander("👤 User Profile"):
                st.write(f"**Email:** {st.session_state['user_email']}")
                if st.button("Update Password"):
                    st.warning("Password update functionality coming soon.")
            
            st.divider()
            if st.button("Log Out"):
                st.session_state['authenticated'] = False
                st.session_state['user_role'] = None
                st.session_state['user_email'] = None
                st.rerun()
        
        # --- MAIN VIEW ---
        st.title("Dashboard Overview")
        if st.session_state['user_role'] == 'executive':
            st.success("Executive Access Granted")
        else:
            st.info("Property Manager Access")

if __name__ == "__main__":
    main()
