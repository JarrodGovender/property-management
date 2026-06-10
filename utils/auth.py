import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    """Initializes the Supabase client using Streamlit secrets."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def login_user(email, password):
    """Authenticates a user and retrieves their role."""
    # Ensure client is in session state
    if 'supabase_client' not in st.session_state:
        st.session_state['supabase_client'] = init_connection()
        
    supabase: Client = st.session_state['supabase_client']
    
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            # Query the custom profiles table for the user's role
            profile_res = supabase.table('profiles').select('role').eq('id', response.user.id).execute()
            role = profile_res.data[0]['role'] if profile_res.data else 'manager'
            return response.user, role
        return None, None
    except Exception as e:
        st.error("Authentication failed. Please check your credentials.")
        return None, None
