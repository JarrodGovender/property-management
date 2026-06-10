import streamlit as st
import sys
import os

# 1. Force Python to recognize the root directory as a path source
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Now import your modules
from utils.auth import init_connection, login_user, signup_user

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Property Operations Tracker",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'supabase_client' not in st.session_state:
    st.session_state['supabase_client'] = init_connection()

# --- MAIN LOGIC ---
def main():
    if not st.session_state['authenticated']:
        st.title("Secure Portal Login")
        
        tab1, tab2 = st.tabs(["Log In", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Log In")
                
                if submit:
                    user, role = login_user(email, password)
                    if user:
                        st.session_state['authenticated'] = True
                        st.session_state['user_role'] = role
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                        
        with tab2:
            st.markdown("### Register New Account")
            with st.form("signup_form"):
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                admin_code = st.text_input("Executive Invite Code (Optional)", type="password")
                signup_submit = st.form_submit_button("Create Account")
                
                if signup_submit:
                    if new_email and new_password:
                        # Define your secret code
                        SECRET_EXECUTIVE_CODE = "PORTFOLIO2026"
                        role = 'executive' if admin_code == SECRET_EXECUTIVE_CODE else 'manager'
                        
                        user, assigned_role = signup_user(new_email, new_password, role)
                        if user:
                            st.success(f"Account created as {assigned_role.capitalize()}! Please log in.")
                    else:
                        st.warning("Please provide email and password.")
    
    else:
        # --- AUTHENTICATED VIEW ---
        st.sidebar.title("Navigation")
        st.sidebar.info(f"Role: {st.session_state['user_role'].capitalize()}")
        
        if st.sidebar.button("Log Out"):
            st.session_state['authenticated'] = False
            st.session_state['user_role'] = None
            st.rerun()
            
        st.title("Dashboard Overview")
        
        # NAVIGATION BASED ON ROLE
        if st.session_state['user_role'] == 'executive':
            st.success("Executive Access Granted")
            st.write("You have full access to the Executive Overview and Archive pages via the sidebar.")
        else:
            st.info("Property Manager Access")
            st.write("Use the 'Site Manager' tab in the sidebar to manage your specific properties.")

if __name__ == "__main__":
    main()
