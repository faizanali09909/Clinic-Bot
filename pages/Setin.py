import streamlit as st
st.set_page_config(page_title="Settings — ClinicBot", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stApp {background: #0a0a0a !important;}
    footer {display: none;}
    </style>
""", unsafe_allow_html=True)
if st.session_state.get("clinic") is None:
    st.switch_page("app.py")
st.markdown("<div style='padding:3rem; color:#fff; font-size:24px; font-weight:600;'>⚙️ Settings — Coming Soon</div>", unsafe_allow_html=True)
if st.button("← Back to Dashboard"):
    st.switch_page("pages/Dashboard.py")