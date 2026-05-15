import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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

    # ---------------- ADMIN DASHBOARD ----------------

st.subheader("📊 Admin Dashboard")

# Pie Chart
fig2, ax2 = plt.subplots()

status_counts = df["Status"].value_counts()

ax2.pie(
    status_counts,
    labels=status_counts.index,
    autopct='%1.1f%%'
)

st.pyplot(fig2)

# Filter Students
filter_option = st.selectbox(
    "Filter Students",
    ["All", "Eligible", "Below 75%"]
)

if filter_option == "Eligible":

    filtered = df[df["Attendance %"] >= 75]

    st.dataframe(filtered)

elif filter_option == "Below 75%":

    filtered = df[df["Attendance %"] < 75]

    st.dataframe(filtered)

else:

    st.dataframe(df)

    # DATABASE CODE HERE
    conn = sqlite3.connect("attendance.db")

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        student TEXT,
        attendance_percent REAL,
        status TEXT
    )
    ''')

    for index, row in df.iterrows():

        cursor.execute('''
        INSERT INTO attendance VALUES (?, ?, ?)
        ''', (
            str(row.iloc[0]),
            row["Attendance %"],
            row["Status"]
        ))

    conn.commit()

    conn.close()

    st.success("✅ Attendance saved to database")

    # ---------------- PDF REPORT ----------------

if st.button("📄 Generate PDF Report"):

    pdf_file = "attendance_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Student Attendance Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 12))

    for index, row in df.iterrows():

        text = (
            f"Student: {row.iloc[0]} | "
            f"Attendance: {row['Attendance %']}% | "
            f"Status: {row['Status']}"
        )

        elements.append(
            Paragraph(text, styles['BodyText'])
        )

        elements.append(Spacer(1, 8))

    doc.build(elements)

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="⬇ Download PDF Report",
            data=file,
            file_name="attendance_report.pdf",
            mime="application/pdf"
        )

else:
    st.warning("Please upload a CSV file.")