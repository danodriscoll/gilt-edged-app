# 2_CMS.py
from datetime import date
import streamlit as st
from st_files_connection import FilesConnection
import duckdb
import plotly.graph_objects as go

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

# Velocity of bills scatter chart (analysis_chart_01)
def analysis_chart_01(df):
    goFig = go.Figure()

    goFig.add_trace(go.Scatter(x=df.date, y=df.velocity_bills,
        mode='lines',
        name='Model Bills'))

    goFig.add_trace(go.Scatter(x=df.date, y=df.velocity_bills_trend,
        mode='lines',
        name='Model Trend'))

    goFig.add_trace(go.Scatter(x=df.date, y=df.yield_rate,
        mode='lines',
        name='Real Yield'))

    goFig.update_layout(
        margin=dict(l=50,r=40,b=40,t=40),
        template="gridon",
        xaxis_title="Financial Quarters",
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Percent',
            titlefont_size=14,
            tickfont_size=12,
        ),
        yaxis_zeroline=False,
        xaxis_zeroline=False,
        showlegend=True,
        legend_title="Analysis Series",
        height=800
    )

    goFig.update_yaxes(
        type="log" if yaxis_type else "linear"
    )

    st.plotly_chart(goFig, use_container_width=True, sharing='streamlit')

if st.session_state.disclaimer_setting:
    with st.status("Importing Data..", expanded=False) as status:
        # Min max date range.
        start_period = "1974-01-01"
        end_period = "2025-12-01"
        # Model output analysis
        st.text("Model Amalysis Time-Series")
        df_model = query_S3(
            "s3://studio-model-analysis/model_lp_analysis/cms_model-analysis-private-1.csv",
            f"SELECT date, velocity_bills, velocity_bills_trend, fiscal_balance, yield_rate FROM df WHERE date >= '{start_period}' AND date <= '{end_period}'"
        )
        status.update(label="Data Imported.", state="complete", expanded=False)

# Layout
header = st.container()
body = st.container()

with header:
    st.header("Contemporary Modern System (CMS)")

with body:
    # Sidebar
    if st.session_state.disclaimer_setting:
        with st.sidebar:
            today = date.today()
            st.write("Today: ", today.strftime('%A %d. %B %Y'))
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
            st.session_state.val_start_date = start_date
            st.session_state.val_end_date = end_date

        df_run_01 = get_fragment(df_model, start_date, end_date)

    # Central
    st.subheader("Velocity of Model Bills Issued")

    if st.session_state.disclaimer_setting:

        min_velocity = "{:0,.3%}".format((df_run_01.velocity_bills.min() / 100))
        max_velocity = "{:0,.3%}".format((df_run_01.velocity_bills.max() / 100))
        mean_velocity = "{:0,.3%}".format((df_run_01.velocity_bills.mean() / 100))

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Finanacial Quarters", len(df_run_01))
        col2.metric("Min Velocity Percent", min_velocity)
        col3.metric("Max Velocity Percent", max_velocity)
        col4.metric("Mean Velocity Percent", mean_velocity)
        
        # st.dataframe(data=df_run_01, hide_index=True, use_container_width=True)
        yaxis_type = st.checkbox(label="Log_yaxis", value=False)
        analysis_chart_01(df_run_01)

    else:
        st.warning("Please read and accept the disclaimer on the Home page.")
