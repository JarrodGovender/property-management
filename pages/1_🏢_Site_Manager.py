import streamlit as st
from utils.db import fetch_all_sites

# Professional 16:9 configuration
st.set_page_config(page_title="Site Manager", layout="wide")

supabase = st.session_state.get('supabase_client')

st.title("🏢 Dealership Site Operations")

# 1. Fetch sites dynamically from database
sites = fetch_all_sites(supabase)

if not sites:
    st.error("No dealership sites found in the database. Please initialize the 'sites' table.")
else:
    # 2. Generate tabs for each dealership
    site_names = [site['name'] for site in sites]
    tabs = st.tabs(site_names)
    
    for i, tab in enumerate(tabs):
        with tab:
            site = sites[i]
            st.subheader(f"Operations: {site['name']}")
            
            # 3. Add Task Interface
            with st.expander("➕ Create New Task", expanded=False):
                with st.form(f"task_form_{site['id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        title = st.text_input("Task Title")
                    with col2:
                        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
                    
                    desc = st.text_area("Task Description")
                    
                    if st.form_submit_button("Submit Task"):
                        supabase.table("tasks").insert({
                            "site_id": site['id'],
                            "title": title,
                            "description": desc,
                            "priority": priority,
                            "status": "Not Started"
                        }).execute()
                        st.success("Task created!")
                        st.rerun()

            # 4. Display Active Tasks and Audit Trail
            st.markdown("---")
            tasks_res = supabase.table("tasks").select("*").eq("site_id", site['id']).neq("status", "Archived").execute()
            
            if tasks_res.data:
                for task in tasks_res.data:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"**{task['title']}**")
                            st.write(task['description'])
                        with col2:
                            st.write(f"Priority: {task['priority']}")
                        with col3:
                            status_options = ["Not Started", "In Progress", "Blocked", "Completed", "Archived"]
                            new_status = st.selectbox(
                                "Status", 
                                status_options, 
                                index=status_options.index(task['status']), 
                                key=f"status_{task['id']}"
                            )
                            if new_status != task['status']:
                                supabase.table("tasks").update({"status": new_status}).eq("id", task['id']).execute()
                                st.rerun()
                        
                        # --- AUDIT TRAIL / NOTES SECTION ---
                        st.markdown("**Audit Trail & Progress Notes**")
                        notes_res = supabase.table("task_notes").select("*").eq("task_id", task['id']).order("created_at", desc=True).execute()
                        
                        for note in notes_res.data:
                            st.caption(f"📅 {note['created_at'][:10]} | {note['note_content']}")
                        
                        new_note = st.text_input("Add a progress note...", key=f"note_input_{task['id']}")
                        if st.button("Post Note", key=f"post_{task['id']}"):
                            if new_note:
                                supabase.table("task_notes").insert({
                                    "task_id": task['id'],
                                    "note_content": new_note
                                }).execute()
                                st.rerun()
            else:
                st.info("No active tasks for this site.")
