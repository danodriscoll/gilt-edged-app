# 2_CMS.py
from datetime import date
import streamlit as st
from st_files_connection import FilesConnection
import duckdb

st.set_page_config(
    layout="wide",
    page_title="Contemporary Modern System",
    menu_items={
        'About': 'https://www.giltedged.net'
    }
)

# Session states
if 'disclaimer_setting' not in st.session_state:
    st.session_state.disclaimer_setting = False

if 'button' not in st.session_state or st.session_state:
    st.session_state.button = False

if 'val_start_date' not in st.session_state:
    st.session_state.val_start_date = date(1974, 1, 1)
    st.session_state.val_end_date = date(2025, 1, 31)


# Functions
def query_S3(file_name, sql):
    # Create connection object and retrieve file contents.
    # Specify input format is a csv and to cache the result for 600 seconds.
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read(file_name, input_format="csv", ttl=600)
    
    # Use DuckDB to filter raw dataframe.
    return duckdb.sql(sql).df()

def get_model_data(file_name, start_period, end_period):
    df = query_S3(
        file_name,
        f"SELECT date, national_income, public_debt FROM df WHERE date >= '{start_period}' AND date <= '{end_period}'"
    )
    return df


# Layout
header = st.container()
body = st.container()
footer = st.container()

with header:
    st.header("Contemporary Modern System (CMS)")
    today = date.today()
    st.write("Today is ", today.strftime('%A %d. %B %Y'), ". The model consumes real-world economic time-series data from 1974 to present day.")

with body:

    if st.session_state.disclaimer_setting:
        with st.sidebar:
            with st.status("Importing Data...", expanded=False) as status:
                st.text("Model Time-Series")
                df_run_01 = get_model_data("s3://studio-model-analysis/model_lp_analysis/df_output.csv", "1974-01-01", "2023-07-01")
                status.update(label="Data Imported.", state="complete", expanded=False)

            st.header("Date Range")
            start_date = st.date_input(
                label="From",
                value=st.session_state.val_start_date,
                min_value=date(1974, 1, 1),
            )
            end_date = st.date_input(
                label="To",
                value=st.session_state.val_end_date,
                max_value=date(2025, 1, 31)
            )

            st.session_state.val_start_date = start_date
            st.session_state.val_end_date = end_date

        if end_date < start_date:
            start_date = date(1974, 1, 1)
            end_date = date(2025, 1, 31)

    st.subheader("System Velocity and the 10-Year Bond Yield")

    if st.session_state.disclaimer_setting:
        st.success("Disclaimer accepted.")
        st.dataframe(data=df_run_01, hide_index=True, use_container_width=True)

    else:
        st.warning("Please read and accept the disclaimer on the Home page.")

with footer:
    st.caption("Footer")