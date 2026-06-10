import streamlit as st
import pandas as pd
from utils.db import get_tasks_with_sites

# Enforce landscape 16:9 presentation for optimal data table viewing
st.set_page_config(
    page_title="Task Archive",
    page_icon="🗄️",
    layout="wide"
)

supabase = st.session_state.get('supabase_client')

st.title("🗄️ Task Archive")
st.markdown("### Historic Property Operations")
st.write("Tasks marked as 'Archived' are stored here permanently for auditing and reference.")

if not supabase:
    st.warning("Please log in to view the archive.")
else:
    df = get_tasks_with_sites(supabase)

    if not df.empty:
        # Filter strictly for archived tasks
        archive_df = df[df['status'] == 'Archived']
        
        if not archive_df.empty:
            # Reorder columns for a cleaner presentation
            display_df = archive_df[['site_name', 'title', 'description', 'priority', 'updated_at']]
            display_df = display_df.rename(columns={
                'site_name': 'Property',
                'title': 'Task',
                'description': 'Details',
                'priority': 'Priority',
                'updated_at': 'Date Archived'
            })
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No historic tasks in the archive yet.")
    else:
        st.info("Database is empty.")
