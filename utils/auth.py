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
    supabase: Client = st.session_state.get('supabase_client')
    if not supabase:
        supabase = init_connection()
        st.session_state['supabase_client'] = supabase
        
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            profile_res = supabase.table('profiles').select('role').eq('id', response.user.id).execute()
            role = profile_res.data[0]['role'] if profile_res.data else 'manager'
            return response.user, role
        return None, None
    except Exception as e:
        return None, None

def signup_user(email, password, role='manager'):
    """Registers a new user and assigns their role in the database."""
    supabase: Client = st.session_state.get('supabase_client')
    if not supabase:
        supabase = init_connection()
        st.session_state['supabase_client'] = supabase
        
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user:
            supabase.table('profiles').insert({
                "id": response.user.id,
                "email": email,
                "role": role
            }).execute()
            return response.user, role
        return None, None
    except Exception as e:
        st.error(f"Sign up error: {e}")
        return None, None
