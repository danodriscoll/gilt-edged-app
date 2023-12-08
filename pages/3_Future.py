# 3_Future.py
import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Agent Expectations",
    menu_items={
        'About': 'https://www.modernmoney.studio'
    }
)

# Session states
if 'disclaimer_setting' not in st.session_state:
    st.session_state.disclaimer_setting = False

if 'button' not in st.session_state or st.session_state:
    st.session_state.button = False

# Layout
header = st.container()
body = st.container()

with header:
    st.header("Model Gilt Future")

    st.write("The model is [evolving](https://www.modernmoney.studio/models/model-future-development#nav-bar). New [parameter settings](https://docs.google.com/document/d/e/2PACX-1vRKFTK0v0LxTWuBPKhmPYTYWqhM_5iq7Wj0zkMvcZUsnYW2Fgywbds50EdbJ3L3YouM-sStQGW5dOoD/pub) may change output and analysis over time.")

    st.write("Beyond consumption of the latest available real-world UK economic time-series data, pure expenditures and interest rates are set by the model logics of both government and central bank agents respectively. View an overview of proposed logic development from the Studio [models](https://www.modernmoney.studio/models/model-future-development#nav-bar) page.")
    st.divider()



with body:
    if st.session_state.disclaimer_setting:
        tab1, tab2 = st.tabs(["Model Yield", "Household Agents"])

        with tab1:
            st.subheader("Model Bond Yield")
            st.success("In development")
        

        with tab2:
            st.subheader("Agent Portfolios")
            st.write("Household agents have bond price expectations. The majority have assumptions about the interest (base) rate in the next step. A minority of agents will be attentive to the macro system velocity and momentum. A record of performance is presented.")
            st.success("In development")

    else:
        st.warning("Please read and accept the disclaimer on the Home page.")

