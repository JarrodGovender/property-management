import streamlit as st
import plotly.express as px
from utils.db import get_tasks_with_sites

# Initialize Supabase client (ensure it's in your session state or imported)
supabase = st.session_state.get('supabase_client')

st.title("Executive Overview")
st.markdown("### Portfolio Task Distribution")

# Fetch Data
df = get_tasks_with_sites(supabase)

if df.empty:
    st.info("No active tasks found in the database. Head to the Site Manager to add tasks.")
else:
    # Filter out archived tasks for the live dashboard
    active_df = df[df['status'] != 'Archived']

    # --- PRIORITY METRIC: Tasks per Site ---
    # Group by site and status to get task counts
    site_task_counts = active_df.groupby(['site_name', 'status']).size().reset_index(name='task_count')
    
    # Create an interactive Plotly stacked bar chart
    fig = px.bar(
        site_task_counts, 
        x='site_name', 
        y='task_count', 
        color='status',
        title="Active Tasks by Property Site",
        labels={'site_name': 'Property', 'task_count': 'Number of Tasks', 'status': 'Task Status'},
        color_discrete_map={
            'Not Started': '#6c757d',
            'In Progress': '#0d6efd',
            'Blocked': '#dc3545',
            'Completed': '#198754'
        }
    )
    
    # Optimize layout for 16:9 executive viewing
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Raw Data Table for deeper inspection
    st.markdown("### Active Task Details")
    st.dataframe(
        active_df[['site_name', 'title', 'status', 'priority', 'created_at']],
        use_container_width=True,
        hide_index=True
    )
