import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attendance Counter with CSV")

st.title("📊 Student Attendance Counter")
st.write("Upload a CSV file to analyze student attendance")

uploaded_file = st.file_uploader("Upload Attendance CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Attendance Data")
    st.dataframe(df)

    # Column 0 -> Student Name / ID
    # Column 1 onwards -> Attendance (1 = Present, 0 = Absent)
    attendance_cols = df.columns[1:]

    # 🔢 INPUT: Total classes conducted
    total_classes = st.number_input(
        "Enter Total Classes Conducted",
        min_value=1,
        value=len(attendance_cols),
        step=1
    )

    # Total attendance per student
    df["Total Attendance"] = df[attendance_cols].sum(axis=1)

    # Attendance percentage (uses input value)
    df["Attendance %"] = (df["Total Attendance"] / total_classes) * 100

    # Eligibility status
    df["Status"] = df["Attendance %"].apply(
        lambda x: "❌ Below 75%" if x < 75 else "✅ Eligible"
    )

    st.subheader("🚦 Attendance Eligibility Table")
    st.dataframe(df)

    # 🔹 COLOR-CODED BAR CHART
    st.subheader("📊 Attendance Percentage per Student")

    colors = ["red" if x < 75 else "green" for x in df["Attendance %"]]

    fig, ax = plt.subplots()
    ax.bar(df.iloc[:, 0], df["Attendance %"], color=colors)

    ax.axhline(75, linestyle="--")  # 75% threshold line
    ax.set_xlabel("Students")
    ax.set_ylabel("Attendance Percentage")
    ax.set_title("Student Attendance (75% Eligibility Rule)")
    ax.set_xticks([])

    st.pyplot(fig)

else:
    st.warning("Please upload a CSV file to proceed.")


    