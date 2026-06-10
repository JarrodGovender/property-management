import streamlit as st
import pandas as pd
from utils.db import get_tasks_with_sites

# Professional 16:9 configuration
st.set_page_config(page_title="Executive Overview", layout="wide")

supabase = st.session_state.get('supabase_client')

st.title("📊 Executive Overview")

# 1. Fetch data
df = get_tasks_with_sites(supabase)

if not df.empty:
    active_df = df[df['status'] != 'Archived']
    
    st.markdown("### Portfolio Task Drill-Down")
    st.write("Select a task below to view the audit trail and post executive updates.")

    # 2. Interactive Selection
    task_titles = active_df['title'].tolist()
    selected_title = st.selectbox("Search/Select Task", task_titles)
    
    # 3. Filter to the selected task
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
        
        # 4. Audit Trail & Executive Input
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
    st.info("No active tasks found in the database.")
