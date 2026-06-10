def signup_user(email, password, role='manager'):
    """Registers a new user and assigns their role in the database."""
    if 'supabase_client' not in st.session_state:
        st.session_state['supabase_client'] = init_connection()
        
    supabase: Client = st.session_state['supabase_client']
    
    try:
        # 1. Create the user credential in Supabase Auth
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        if response.user:
            # 2. Link their new Auth ID to our custom profiles table with their role
            supabase.table('profiles').insert({
                "id": response.user.id,
                "email": email,
                "role": role
            }).execute()
            
            return response.user, role
            
        return None, None
    except Exception as e:
        # Supabase will catch errors like "User already exists" or "Password too weak"
        st.error(f"Sign up failed: {e}")
        return None, None
