import streamlit as st
import pandas as pd
import json
import os
import subprocess
from datetime import datetime

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHANGES_FILE = os.path.join(BASE_DIR, "reports", "changes.json")
HISTORY_FILE = os.path.join(BASE_DIR, "reports", "history.json")

# ---------------------------------------------------
# Streamlit Page
# ---------------------------------------------------

st.set_page_config(
    page_title="GitHub Change Dashboard",
    layout="wide"
)

st.title("🚀 GitHub Change Dashboard")

# ---------------------------------------------------
# Refresh Button
# ---------------------------------------------------

col1, col2 = st.columns([1,5])

with col1:

    if st.button("🔄 Refresh"):

        subprocess.run(
            ["python", os.path.join(BASE_DIR, "scripts", "run_pipeline.py")]
        )

        st.rerun()

with col2:

    st.write(f"Last opened : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

# ---------------------------------------------------
# Load JSON
# ---------------------------------------------------

if not os.path.exists(CHANGES_FILE):

    st.error("Run the pipeline first.")

    st.stop()

with open(CHANGES_FILE) as f:

    data = json.load(f)

# ---------------------------------------------------
# Repository Information
# ---------------------------------------------------

st.divider()

st.subheader("Repository Information")

c1,c2,c3,c4 = st.columns(4)

c1.metric("Repository", data["repository"])
c2.metric("Branch", data["branch"])
c3.metric("Latest Commit", data["latest_commit"][:8])
c4.metric("Previous Commit", data["previous_commit"][:8])

c5,c6,c7 = st.columns(3)

c5.metric("Author", data["author"])
c6.metric("Commit Time", data["commit_time"])
c7.metric("Pipeline Time", data["pipeline_time"])

st.info(data["message"])

# ---------------------------------------------------
# Changed Files
# ---------------------------------------------------

st.divider()

st.subheader("📂 Changed Files")

files = pd.DataFrame(data["files"])

search = st.text_input("Search File")

if search:

    files = files[
        files["filename"].str.contains(search, case=False)
    ]

st.dataframe(
    files[
        [
            "filename",
            "status",
            "additions",
            "deletions",
            "changes"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------------------
# Line Changes
# ---------------------------------------------------

st.divider()

st.subheader("📝 Line Changes")

lines = pd.DataFrame(data["line_changes"])

if len(lines):

    st.dataframe(
        lines,
        use_container_width=True
    )

else:

    st.success("No line changes detected.")

# ---------------------------------------------------
# History
# ---------------------------------------------------

st.divider()

st.subheader("📜 Pipeline History")

if os.path.exists(HISTORY_FILE):

    with open(HISTORY_FILE) as f:

        history = json.load(f)

    rows = []

    for item in reversed(history):

        rows.append({

            "Repository": item["repository"],

            "Commit": item["latest_commit"][:8],

            "Author": item["author"],

            "Time": item["commit_time"],

            "Message": item["message"],

            "Files": len(item["files"])

        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )