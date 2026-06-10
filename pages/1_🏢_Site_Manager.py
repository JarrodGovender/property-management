import streamlit as st
from utils.db import fetch_all_sites

supabase = st.session_state.get('supabase_client')

st.title("Property Site Manager")

# Fetch dynamic sites
sites = fetch_all_sites(supabase)

if not sites:
    st.warning("No sites configured. Please add sites to the database.")
else:
    # Extract names and create dynamic tabs
    site_names = [site['name'] for site in sites]
    site_tabs = st.tabs(site_names)
    
    for index, tab in enumerate(site_tabs):
        with tab:
            current_site = sites[index]
            st.markdown(f"### Manage Operations: {current_site['name']}")
            
            # Form to add a new task for this specific site
            with st.expander(f"➕ Add New Task for {current_site['name']}", expanded=False):
                with st.form(key=f"form_{current_site['id']}"):
                    task_title = st.text_input("Task Title")
                    task_desc = st.text_area("Description")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        task_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
                    with col2:
                        task_status = st.selectbox("Status", ["Not Started", "In Progress", "Blocked", "Completed"])
                        
                    submit_task = st.form_submit_button("Create Task")
                    
                    if submit_task and task_title:
                        # Insert into Supabase
                        data, count = supabase.table('tasks').insert({
                            "site_id": current_site['id'],
                            "title": task_title,
                            "description": task_desc,
                            "priority": task_priority,
                            "status": task_status
                            # 'created_by' would use st.session_state['user_id']
                        }).execute()
                        st.success("Task added successfully!")
                        st.rerun()

            st.divider()
            
            # Here you would query and display the active tasks specifically for `current_site['id']`
            # and provide an interface to add notes to them.
           # Fetch active tasks for this specific site
            tasks_response = supabase.table('tasks').select('*').eq('site_id', current_site['id']).neq('status', 'Archived').execute()
            site_tasks = tasks_response.data
            
            if site_tasks:
                st.markdown("#### Current Tasks")
                for task in site_tasks:
                    with st.expander(f"📌 {task['title']} - [{task['status']}]"):
                        st.write(f"**Description:** {task['description']}")
                        
                        # Status Update
                        col_status, col_empty = st.columns([1, 2])
                        with col_status:
                            status_options = ["Not Started", "In Progress", "Blocked", "Completed", "Archived"]
                            new_status = st.selectbox(
                                "Update Status", 
                                status_options, 
                                index=status_options.index(task['status']), 
                                key=f"status_{task['id']}"
                            )
                            
                            if new_status != task['status']:
                                supabase.table('tasks').update({'status': new_status}).eq('id', task['id']).execute()
                                st.success(f"Task marked as {new_status}!")
                                st.rerun()

                        st.divider()
                        
                        # Dated Notes Section
                        st.markdown("**Progress Notes**")
                        notes_response = supabase.table('task_notes').select('*').eq('task_id', task['id']).order('created_at', desc=True).execute()
                        
                        for note in notes_response.data:
                            # Slice the timestamp to show just the date (YYYY-MM-DD)
                            st.caption(f"Logged on: {note['created_at'][:10]}")
                            st.info(note['note_content'])
                        
                        # Add a new note
                        new_note = st.text_input("Add a progress update...", key=f"note_input_{task['id']}")
                        if st.button("Save Note", key=f"save_note_{task['id']}"):
                            if new_note:
                                supabase.table('task_notes').insert({
                                    "task_id": task['id'],
                                    "note_content": new_note
                                }).execute()
                                st.rerun()
            else:
                st.info("No active tasks for this site. Enjoy the downtime.")
