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
    st.session_state.val_end_date = date(2025, 1, 1)


# Functions
def query_S3(file_name, sql):
    # Create connection object and retrieve file contents.
    # Specify input format is a csv and to cache the result for 900 seconds.
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read(file_name, input_format="csv", ttl=900)
    
    # Use DuckDB to filter raw dataframe.
    return duckdb.sql(sql).df()

# Filter random historical time-series data.
def get_fragment(df, start, end):
    sql = f"SELECT * FROM df WHERE date >= '{start}' AND date <= '{end}'"
    return duckdb.sql(sql).df()


if st.session_state.disclaimer_setting:
    with st.status("Importing Data..", expanded=False) as status:
        # Min max date range.
        start_period = "1974-01-01"
        end_period = "2025-12-01"
        # Model output analysis
        st.text("Model Time-Series")
        df_model = query_S3(
            "s3://studio-model-analysis/model_lp_analysis/cms_model-analysis-private-1.csv",
            f"SELECT date, velocity_bills, velocity_bills_trend, fiscal_balance FROM df WHERE date >= '{start_period}' AND date <= '{end_period}'"
        )
        status.update(label="Data Imported.", state="complete", expanded=False)

# Layout
header = st.container()
body = st.container()
footer = st.container()

with header:
    st.header("Contemporary Modern System (CMS)")
    today = date.today()
    st.write("Today is ", today.strftime('%A %d. %B %Y'), ". The model consumes real-world economic time-series data from 1974 to present day.")

with body:
    # Sidebar
    if st.session_state.disclaimer_setting:
        with st.sidebar:
            st.header("Date Range")
            start_date = st.date_input(
                label="From",
                value=st.session_state.val_start_date,
                min_value=date(1974, 1, 1),
                max_value=date(2020, 1, 1)
            )
            end_date = st.date_input(
                label="To",
                value=st.session_state.val_end_date,
                min_value=date(1978, 1, 1),
                max_value=date(2025, 1, 1)
            )

            st.session_state.val_start_date = start_date
            st.session_state.val_end_date = end_date

        if end_date < start_date:
            start_date = date(1974, 1, 1)
            end_date = date(2025, 1, 1)

        df_run_01 = get_fragment(df_model, start_date, end_date)

    # Central
    st.subheader("Central")

    if st.session_state.disclaimer_setting:

        curr_symbol = "£"
        min_balance = curr_symbol + "{:0,.0f}".format(df_run_01.fiscal_balance.min())
        max_balance = curr_symbol + "{:0,.0f}".format(df_run_01.fiscal_balance.max())
        mean_balance = curr_symbol + "{:0,.0f}".format(df_run_01.fiscal_balance.mean())

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Finanacial Quarters", len(df_run_01))
        col2.metric("Min Fiscal Balance", min_balance)
        col3.metric("Max Fiscal Balance", max_balance)
        col4.metric("Mean Fiscal Balance", mean_balance)
        
        st.dataframe(data=df_run_01, hide_index=True, use_container_width=True)

    else:
        st.warning("Please read and accept the disclaimer on the Home page.")

with footer:
    st.caption("Footer")