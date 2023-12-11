# Home.py
import streamlit as st

st.set_page_config(
    layout="centered",
    page_title="Home",
    menu_items={
        'About': 'https://www.modernmoney.studio'
    }
)

# Session states
if 'disclaimer_setting' not in st.session_state:
    st.session_state.disclaimer_setting = False

if 'disclaimer_checkbox' in st.session_state:
    if st.session_state.disclaimer_checkbox:
        st.session_state.disclaimer_setting = True
    else:
        st.session_state.disclaimer_setting = False
else:
    st.session_state.disclaimer_checkbox = False

if 'button' not in st.session_state or st.session_state:
    st.session_state.button = False

# Layout
header = st.container()
body = st.container()
footer = st.container()

with header:
    st.title("Gilt Edged App")
    st.info("The app may change, break, or disappear at any time.")
    st.write("Visit [GiltEdged.net](https://www.giltedged.net). Part of a self-directed learning [project](https://www.modernmoney.studio).")

    st.header("About")
    st.write("A Gilt edged context. View the [system analysis](https://docs.google.com/document/d/e/2PACX-1vToO3up00d3X2-iLzHBb4JNghWuy-miJkGGo5CY-tZbLyN-iAzbT_A4A_IeZ9YLenqA6-3PdFNoel1Y/pub) document for model features and overview.")

with body:
    st.subheader("Early Modern System (EMS)")
    st.write("The velocity of a model monetary system in a British military and economic context. The model consumes real-world economic time-series data from 1694 to 1972.")

    st.subheader("Contemporary Modern System (CMS)")
    st.write("The model consumes real-world economic time-series data from 1974 to present day. Analysis is stripped of payments on interest-bearing bills and consols held.")


    st.subheader("Disclaimer")
    with st.expander(label="Disclaimer Message", expanded=True):
        st.write("The web app and the information contained herein is not intended to be a source of advice or credit analysis with respect to the material presented, and the information and / or documents contained in this web app do not constitute investment advice.")
    
    if not st.session_state.disclaimer_setting:
        st.warning("Disclaimer not accepted.")
        st.checkbox(label="I have read and accept the disclaimer.", value=st.session_state.disclaimer_setting, key="disclaimer_checkbox")
    else:
        st.success("Disclaimer accepted.")


with footer:
    st.caption("Footer")
