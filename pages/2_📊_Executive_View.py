import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_tasks_with_sites

st.set_page_config(page_title="Executive Overview", layout="wide")

supabase = st.session_state.get('supabase_client')

st.title("📊 Executive Overview")

# Fetch data
df = get_tasks_with_sites(supabase)

if not df.empty:
    active_df = df[df['status'] != 'Archived']

    # --- EXECUTIVE HEALTH SUMMARY ---
    st.markdown("### Portfolio Health Summary")
    
    total_tasks = len(active_df)
    priority_counts = active_df['priority'].value_counts().reindex(['Urgent', 'High', 'Medium', 'Low'], fill_value=0)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Active Tasks", total_tasks)
    col2.metric("Urgent", priority_counts['Urgent'])
    col3.metric("High", priority_counts['High'])
    col4.metric("Medium", priority_counts['Medium'])
    col5.metric("Low", priority_counts['Low'])

    st.divider()

    # --- TASKS PER SITE BREAKDOWN ---
    st.markdown("### Workload Distribution by Site")
    site_counts = active_df['site_name'].value_counts().reset_index()
    site_counts.columns = ['Site', 'Task Count']
    
    fig = px.bar(site_counts, x='Site', y='Task Count', color='Task Count',
                 color_continuous_scale='Blues', text='Task Count')
    fig.update_layout(height=400, margin=dict(t=30, b=30))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- DRILL-DOWN SECTION ---
    st.markdown("### Task Drill-Down")
    
    task_titles = active_df['title'].tolist()
    selected_title = st.selectbox("Search/Select Task", task_titles)
    
    selected_task = active_df[active_df['title'] == selected_title].iloc[0]
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(selected_task['title'])
            st.write(f"**Site:** {selected_task['site_name']}")
            st.write(f"**Description:** {selected_task['description']}")
        with col2:
            st.info(f"**Status:** {selected_task['status']}")
            st.write(f"**Priority:** {selected_task['priority']}")
            
        st.markdown("---")
        
        st.markdown("**Audit Trail**")
        notes_res = supabase.table("task_notes").select("*").eq("task_id", selected_task['id']).order("created_at", desc=True).execute()
        
        for note in notes_res.data:
            st.caption(f"📅 {note['created_at'][:10]} | {note['note_content']}")
            
        new_note = st.text_input("Post Executive Note", key="exec_note")
        if st.button("Submit Executive Update"):
            if new_note:
                supabase.table("task_notes").insert({
                    "task_id": selected_task['id'],
                    "note_content": f"[EXEC NOTE] {new_note}"
                }).execute()
                st.rerun()
else:
    st.info("No active tasks found in the database. Head to the Site Manager to begin operations.")
