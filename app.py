import streamlit as st
from utils.auth import login_user, signup_user

# Enforce professional landscape layout
st.set_page_config(
    page_title="Property Operations Tracker",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

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
                    # Logic calls utils/auth.py interacting with Supabase
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
                new_password = st.text_input("Password", type="password", help="Must be at least 6 characters.")
                
                # The invite code determines the user's role
                admin_code = st.text_input("Executive Invite Code (Optional)", type="password", help="Leave blank for standard Property Manager access.")
                
                signup_submit = st.form_submit_button("Create Account")
                
                if signup_submit:
                    if new_email and new_password:
                        # Define the secret code (In production, move this to secrets.toml)
                        SECRET_EXECUTIVE_CODE = "PORTFOLIO2026" 
                        
                        assigned_role = 'manager'
                        if admin_code == SECRET_EXECUTIVE_CODE:
                            assigned_role = 'executive'
                            
                        # Call the backend function
                        user, role = signup_user(new_email, new_password, assigned_role)
                        
                        if user:
                            st.success(f"Account created successfully as {assigned_role.capitalize()}! Please switch to the Log In tab.")
                    else:
                        st.warning("Please provide both an email and a password.")
    
    else:
        st.sidebar.success(f"Logged in successfully.")
        if st.sidebar.button("Log Out"):
            st.session_state['authenticated'] = False
            st.session_state['user_role'] = None
            st.rerun()
            
        st.title("Dashboard Overview")
        st.write("Please navigate using the sidebar to view Site Management or Executive Reports.")

if __name__ == "__main__":
    main()
