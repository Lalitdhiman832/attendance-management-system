import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Attendance System",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOGIN SYSTEM ----------------

username = st.sidebar.text_input("Username")

password = st.sidebar.text_input(
    "Password",
    type="password"
)

if username != "admin" or password != "1234":
    st.warning("Invalid login credentials")
    st.stop()

# Sidebar
st.sidebar.title("📚 Attendance Dashboard")

# Title
st.title("📊 Student Attendance Counter")
st.write("Upload a CSV file to analyze attendance")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Attendance CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Attendance Data")
    st.dataframe(df)

    attendance_cols = df.columns[1:]

    total_classes = len(attendance_cols)

    # Total Attendance
    df["Total Attendance"] = df[attendance_cols].sum(axis=1)

    # Attendance Percentage
    df["Attendance %"] = round(
        (df["Total Attendance"] / total_classes) * 100,
        2
    )

    # Status
    df["Status"] = df["Attendance %"].apply(
        lambda x: "❌ Below 75%" if x < 75 else "✅ Eligible"
    )

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", len(df))

    col2.metric(
        "Eligible",
        len(df[df["Attendance %"] >= 75])
    )

    col3.metric(
        "Below 75%",
        len(df[df["Attendance %"] < 75])
    )

    # Search
    search = st.text_input("🔍 Search Student")

    if search:
        filtered_df = df[
            df.iloc[:, 0].astype(str).str.contains(search, case=False)
        ]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)

    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download Attendance Report",
        data=csv,
        file_name="attendance_report.csv",
        mime="text/csv"
    )

    # Graph
    st.subheader("📊 Attendance Graph")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(df.iloc[:, 0], df["Attendance %"])

    ax.axhline(75, linestyle="--")

    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
    st.warning("Please upload a CSV file.")