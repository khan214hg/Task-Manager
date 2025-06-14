import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

FILE_NAME = "tasks.csv"

# Check file or create/reset if structure wrong
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    if "Date" not in df.columns or "Task" not in df.columns or "Status" not in df.columns:
        df = pd.DataFrame(columns=["Date", "Task", "Status"])
        df.to_csv(FILE_NAME, index=False)
else:
    df = pd.DataFrame(columns=["Date", "Task", "Status"])
    df.to_csv(FILE_NAME, index=False)

st.title("Daily Task Manager")

# Sidebar date dropdown
if not df.empty:
    date_options = sorted(df["Date"].unique(), reverse=True)
else:
    date_options = [date.today().isoformat()]

selected_date = st.sidebar.selectbox("Select Date", date_options)

# Add task form
st.subheader("Add New Task")
with st.form("add_task_form"):
    task = st.text_input("Task Description")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if task:
            today = date.today().isoformat()
            new_row = {"Date": today, "Task": task, "Status": "Pending"}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("Task added!")
            st.experimental_rerun()  # Refresh app to update sidebar
        else:
            st.warning("Please enter a task description.")

# Filter tasks for selected date
filtered_df = df[df["Date"] == selected_date]

st.subheader(f"Tasks for {selected_date}")
st.dataframe(filtered_df)

# Reset button
if st.button("Reset All Tasks", key="reset_button"):
    df = pd.DataFrame(columns=["Date", "Task", "Status"])
    df.to_csv(FILE_NAME, index=False)
    st.success("All tasks have been reset!")
    st.experimental_rerun()


FILE_NAME = "tasks.csv"

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=["Task", "Status"])

st.title("Mini To-Do List")

# Add task
st.subheader("Add New Task")
with st.form("task_form"):
    task = st.text_input("Task Description")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if task:
            new_row = {"Task": task, "Status": "Pending"}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("Task added!")
        else:
            st.warning("Please enter a task description.")

# Mark complete
st.subheader("Mark Task as Completed")
task_to_complete = st.selectbox("Select task", df[df["Status"] == "Pending"]["Task"].tolist())
if st.button("Mark Completed"):
    df.loc[df["Task"] == task_to_complete, "Status"] = "Completed"
    df.to_csv(FILE_NAME, index=False)
    st.success(f'Task "{task_to_complete}" marked as completed!')

# Reset task list
st.subheader("Reset Tasks List")
if st.button("Reset All Tasks"):
    df = pd.DataFrame(columns=["Task", "Status"])
    df.to_csv(FILE_NAME, index=False)
    st.success("All tasks have been reset!")

# Show all tasks
today = date.today().isoformat()
today_df = df[df["Date"] == today]

st.subheader(f"Today's Tasks ({today})")
st.dataframe(today_df)

if st.button("Show Yesterday's Tasks"):
    from datetime import timedelta
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    yest_df = df[df["Date"] == yesterday]
    if not yest_df.empty:
        st.subheader(f"Yesterday's Tasks ({yesterday})")
        st.dataframe(yest_df)
    else:
        st.info("No tasks found for yesterday.")

# Download button
st.download_button("Download Tasks CSV", df.to_csv(index=False), file_name="tasks.csv")
