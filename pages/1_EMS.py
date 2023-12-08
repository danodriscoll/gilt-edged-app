# 1_EMS.py
import random
import time
from datetime import date
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd
import duckdb
import plotly.graph_objects as go

st.set_page_config(
    layout="wide",
    page_title="Early Modern System",
    menu_items={
        'About': 'https://www.giltedged.net'
    }
)

# Session states
if 'button' not in st.session_state:
    st.session_state.button = False

# Functions
def query_S3(file_name, sql):
    # Create connection object and retrieve file contents.
    # Specify input format is a csv and to cache the result for 600 seconds.
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read(file_name, input_format="csv", ttl=900)
    
    # Use DuckDB to filter raw dataframe.
    return duckdb.sql(sql).df()

@st.cache_data
def load_events(url, rows):
    df = pd.read_csv(url, nrows=rows)
    return df

# Filter random historical time-series data.
def get_fragment(df, start, end):
    sql = f"SELECT * FROM df WHERE date >= '{start}' AND date <= '{end}'"
    return duckdb.sql(sql).df()

# Toast message random date chosen.
def range_toast(d_begin, d_end):
    msg = st.toast('Choosing Date Range..')
    time.sleep(1)
    msg.toast(f"From: {d_begin.strftime('%A %d. %b %Y')}.")
    time.sleep(1)
    msg.toast(f"To: {d_end.strftime('%A %d. %b %Y')}.")

def click_button():
    st.session_state.button = not st.session_state.button

# Velocity of bills scatter chart
def velocity_scatter(df):
    goFig = go.Figure()
    goFig.add_trace(go.Scatter(x=df_model_fragment.date, y=df_model_fragment.velocity_bills,
        mode='lines+markers+text',
        line_color='#FF5733',
        name='Velocity Bills',
        text=round(df_model_fragment.velocity_bills, 2),
        textposition="top center",
        line_shape="spline"
    ))
    goFig.add_trace(go.Scatter(x=df_model_fragment.date, y=df_model_fragment.velocity_bills_trend,
        mode='lines+markers+text',
        line_color='#008080',
        name='Long Trend',
        line_shape="spline"
    ))

    goFig.update_layout(
        height=450,
        margin=dict(l=50,r=40,b=40,t=40),
        template="gridon",
        xaxis_title="Financial Years",
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Velocity of Bills Percent',
            titlefont_size=14,
            tickfont_size=12,
        ),
        showlegend=True,
    )

    st.plotly_chart(goFig, use_container_width=True, sharing='streamlit')

# Fiscal balance chart
def fiscal_bar(df):
    goFig = go.Figure()
    values = list(df.iloc[:,1]) # Create a list of 'fiscal_balance' values.
    goFig.add_trace(go.Bar(x=df.date, y=df.fiscal_balance,
        marker=dict(
            color=values,
            colorscale="Rdbu",
        )
    ))

    goFig.update_layout(
        margin=dict(l=50,r=40,b=40,t=40),
        template="gridon",
        xaxis_title="Financial Quarters",
        xaxis_tickfont_size=12,
        yaxis=dict(
            title="Flow of Money Bills",
            titlefont_size=14,
            tickfont_size=12,
        ),
        showlegend=False,
        legend_title="Legend",
        height=450
    )

    st.plotly_chart(goFig, use_container_width=True, sharing='streamlit')

# Layout
header = st.container()
body = st.container()

with header:
    col1, col2 = st.columns([3,2], gap="small")

    with col1:
        st.header("Early Modern System (EMS)")
        st.write("The historical velocity of the monetary system in a British military and economic context.")
        with st.status("Importing Data..", expanded=False) as status:            
            # Min max date range.
            start_period = "1698-01-01"
            end_period = "1974-12-01"
            # Model output analysis
            st.text("Model Time-Series")
            df_model = query_S3(
                "s3://studio-model-analysis/model_lp_analysis/ems_model-analysis-private-1.csv",
                f"SELECT date, velocity_bills, velocity_bills_trend, fiscal_balance FROM df WHERE date >= '{start_period}' AND date <= '{end_period}'"
            )
            # Period events
            st.text("Events Time-Series")
            df_events = load_events(
                "https://huggingface.co/datasets/DanODrisc/gilt_edged/raw/main/ems_events",
                1000 # number of events across the period.
            )
            status.update(label="Data Imported.", state="complete", expanded=False)

    with col2:
        with st.container(border=True):
            st.subheader("Historical Date Range", divider="grey")
            st.write("Generate a random view, charts and events, of UK History.")
            st.button("Spin Date Range", type="primary", on_click=click_button, disabled=st.session_state.button)


with body:
    st.subheader("Chart & Events", divider="violet")

    placeholder = st.empty()
    placeholder.markdown("Reflecting on the past to inform the present and future. View the [Millennium Dataset](https://www.bankofengland.co.uk/statistics/research-datasets).")

    if st.session_state.button:
        with st.spinner(text="Selecting historical data.."):
            year = random.randint(1698, 1955)
            month = 1
            day = 1        
            start_date = date(year, month, day)
            end_date = date(start_date.year + 20, month, day)
            range_toast(start_date, end_date)
            df_model_fragment = get_fragment(df_model, start_date, end_date)
            df_events_fragment = get_fragment(df_events, start_date, end_date)
        
        with placeholder.container(border=True):
            st.write("From: ", start_date.strftime('%A %d. %B %Y'), start_date, "To: ", end_date.strftime('%A %d. %B %Y'), end_date)
            tab1, tab2 = st.tabs(["Velocity Bills", "Fiscal Balance"])
            with tab1:
                velocity_scatter(df_model_fragment)            

            with tab2:
                fiscal_bar(df_model_fragment)

            st.dataframe(data=df_events_fragment, column_config={"date": "Date", "event": "Event"}, hide_index=True, use_container_width=True)

    # Reset page button.
    if st.session_state.button:
        st.button("Clear Date Range", on_click=click_button)
