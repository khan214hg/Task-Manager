import streamlit as st
import pandas as pd
import os

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
st.subheader("All Tasks")
st.dataframe(df)

# Download button
st.download_button("Download Tasks CSV", df.to_csv(index=False), file_name="tasks.csv")
