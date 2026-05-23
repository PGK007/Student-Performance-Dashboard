import streamlit as st
import pandas as pd
import plotly.express as px
import random

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOGIN SYSTEM
# =====================================================

USERNAME = "Admin"
PASSWORD = "GNU@2026"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Student Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.stop()

# =====================================================
# THEME TOGGLE
# =====================================================

dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# TITLE
# =====================================================

st.title("📊 Student Performance Dashboard")
st.subheader("Guru Nanak University")

st.markdown("---")

# =====================================================
# FILE UPLOADER
# =====================================================

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data(file):

    return pd.read_csv(file)

if uploaded_file is not None:

    df = load_data(uploaded_file)

else:

    df = pd.read_csv("students.csv")

# =====================================================
# SUBJECTS
# =====================================================

subjects = [
    "Maths",
    "Physics",
    "Chemistry",
    "English",
    "Computer"
]

# =====================================================
# CALCULATIONS
# =====================================================

df["Total"] = df[subjects].sum(axis=1)

df["Average"] = round(
    df[subjects].mean(axis=1),
    2
)

df["CGPA"] = round(
    df["Average"] / 9.5,
    2
)

# =====================================================
# RANK SYSTEM
# =====================================================

df["Rank"] = df["Average"].rank(
    ascending=False,
    method="dense"
).astype(int)

# =====================================================
# ATTENDANCE
# =====================================================

df["Attendance"] = [
    random.randint(65, 100)
    for i in range(len(df))
]

# =====================================================
# SIDEBAR MENU
# =====================================================

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Student Details",
        "Graphs",
        "Leaderboard",
        "Pass/Fail",
        "Attendance"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.header("📋 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Students",
        len(df)
    )

    col2.metric(
        "Class Average",
        round(df["Average"].mean(), 2)
    )

    col3.metric(
        "Top Score",
        df["Average"].max()
    )

    col4.metric(
        "Lowest Score",
        df["Average"].min()
    )

    st.markdown("---")

    st.subheader("Student Database")

    search = st.text_input(
        "🔍 Search Student"
    )

    if search:

        filtered_df = df[
            df["Name"].str.contains(
                search,
                case=False
            )
        ]

        st.dataframe(filtered_df)

    else:

        st.dataframe(df)

# =====================================================
# STUDENT DETAILS
# =====================================================

elif menu == "Student Details":

    st.header("👨‍🎓 Student Details")

    student_name = st.selectbox(
        "Select Student",
        df["Name"]
    )

    student_data = df[
        df["Name"] == student_name
    ]

    st.dataframe(student_data)

    st.subheader("Performance Progress")

    for sub in subjects:

        mark = int(
            student_data[sub].values[0]
        )

        st.write(f"{sub}: {mark}")

        st.progress(mark)

    # PERFORMANCE PREDICTION

    avg = student_data["Average"].values[0]

    st.subheader("Prediction")

    if avg >= 90:

        st.success("Excellent Performance")

    elif avg >= 75:

        st.info("Good Performance")

    else:

        st.warning("Needs Improvement")

# =====================================================
# GRAPHS
# =====================================================

elif menu == "Graphs":

    st.header("📊 Interactive Graphs")

    graph_option = st.selectbox(
        "Select Graph",
        [
            "Bar Chart",
            "Line Graph",
            "Pie Chart"
        ]
    )

    # BAR CHART

    if graph_option == "Bar Chart":

        fig = px.bar(
            df,
            x="Name",
            y="Average",
            color="Average",
            title="Student Average Marks"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # LINE GRAPH

    elif graph_option == "Line Graph":

        fig = px.line(
            df,
            x="Name",
            y="Average",
            markers=True,
            title="Performance Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # PIE CHART

    elif graph_option == "Pie Chart":

        subject_avg = df[subjects].mean()

        pie_df = pd.DataFrame({
            "Subject": subjects,
            "Average": subject_avg
        })

        fig = px.pie(
            pie_df,
            names="Subject",
            values="Average",
            title="Subject Contribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =====================================================
# LEADERBOARD
# =====================================================

elif menu == "Leaderboard":

    st.header("🏆 Top Students")

    top_students = df.sort_values(
        by="Average",
        ascending=False
    )

    st.dataframe(
        top_students[
            [
                "Rank",
                "Name",
                "Average",
                "CGPA"
            ]
        ]
    )

# =====================================================
# PASS FAIL
# =====================================================

elif menu == "Pass/Fail":

    st.header("✅ Pass / Fail Statistics")

    pass_mark = st.slider(
        "Select Pass Mark",
        35,
        100,
        40
    )

    df["Status"] = df[subjects].apply(
        lambda row:
        "Pass"
        if all(mark >= pass_mark for mark in row)
        else "Fail",
        axis=1
    )

    st.dataframe(
        df[
            [
                "Name",
                "Status"
            ]
        ]
    )

    pass_count = (
        df["Status"] == "Pass"
    ).sum()

    fail_count = (
        df["Status"] == "Fail"
    ).sum()

    pie_df = pd.DataFrame({
        "Status": ["Pass", "Fail"],
        "Count": [pass_count, fail_count]
    })

    fig = px.pie(
        pie_df,
        names="Status",
        values="Count",
        title="Pass/Fail Ratio"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# ATTENDANCE
# =====================================================

elif menu == "Attendance":

    st.header("🧾 Attendance Section")

    student = st.selectbox(
        "Select Student ",
        df["Name"]
    )

    attendance = df[
        df["Name"] == student
    ]["Attendance"].values[0]

    st.write(
        f"Attendance: {attendance}%"
    )

    st.progress(
        int(attendance)
    )

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

st.sidebar.markdown("---")

csv = df.to_csv(index=False)

st.sidebar.download_button(
    label="📥 Download Report",
    data=csv,
    file_name="student_report.csv",
    mime="text/csv"
)