import pandas as pd
import streamlit as st

# Assuming supabase client is initialized elsewhere and passed in or imported
# from supabase import create_client

def get_tasks_with_sites(supabase):
    """Fetches all tasks joined with their respective site names."""
    response = supabase.table("tasks").select("*, sites(name)").execute()
    
    if not response.data:
        return pd.DataFrame()
        
    # Flatten the nested site name dictionary returned by Supabase
    df = pd.DataFrame(response.data)
    df['site_name'] = df['sites'].apply(lambda x: x['name'] if x else 'Unknown')
    df = df.drop(columns=['sites'])
    
    return df

def fetch_all_sites(supabase):
    """Fetches the list of all property sites."""
    response = supabase.table("sites").select("*").execute()
    return response.data
