import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import login_clinic

st.set_page_config(
    page_title="Login — ClinicBot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
    * { outline: none !important; box-shadow: none !important; }
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stApp {background: #0a0a0a !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    footer {display: none;}

    .stTextInput input {
        background: #1a1a1a !important;
        border: 0.5px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #e8e6e1 !important;
        font-size: 14px !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
    }
    .stTextInput input:focus {
        border: 0.5px solid #7f77dd !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
    }
    .stTextInput input:invalid {
        border: 0.5px solid #2a2a2a !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
    }
    .stTextInput input:-webkit-autofill {
        -webkit-box-shadow: 0 0 0px 1000px #1a1a1a inset !important;
        -webkit-text-fill-color: #e8e6e1 !important;
    }
    .stTextInput > div, .stTextInput > div > div {
        outline: none !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
        border: none !important;
    }
    .stTextInput > div:focus-within {
        outline: none !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
    }
    .stTextInput label { color: #aaa !important; font-size: 13px !important; }

    .stButton button {
        background: #7f77dd !important;
        border: none !important;
        color: #fff !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .stButton button:hover { background: #6d65cc !important; }

    div[data-testid="column"]:nth-child(2) .stButton button {
        background: transparent !important;
        border: 0.5px solid #333 !important;
        color: #ccc !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 400 !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton button:hover {
        border-color: #7f77dd !important;
        color: #fff !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.get("clinic") is not None:
    st.switch_page("pages/home.py")

# ── Navbar ──
col1, col2 = st.columns([9, 1])
with col1:
    st.markdown("<div style='padding:14px 0; font-size:20px; font-weight:600; color:#fff;'><span style='color:#7f77dd'>Clinic</span>Bot</div>", unsafe_allow_html=True)
with col2:
    if st.button("← Home", key="nav_home"):
        st.switch_page("app.py")

st.markdown("<hr style='border:none; border-top:0.5px solid #2a2a2a; margin:0 0 2rem 0;'>", unsafe_allow_html=True)

_, card_col, _ = st.columns([1, 2, 1])

with card_col:
    st.markdown("""
        <div style='text-align:center; margin-bottom:0.5rem;'>
            <span style='font-size:22px; font-weight:600; color:#fff;'>Welcome back</span>
        </div>
        <div style='text-align:center; font-size:13px; color:#666; margin-bottom:1.5rem;'>
            Login to your ClinicBot account
        </div>
    """, unsafe_allow_html=True)

    email    = st.text_input("Email Address", placeholder="you@clinic.com")
    password = st.text_input("Password", placeholder="Your password", type="password")

    if st.button("Login →", use_container_width=True, key="login_btn"):
        if not email or not password:
            st.error("Please fill in all fields.")
        else:
            clinic = login_clinic(email, password)
            if clinic:
                st.session_state.clinic = clinic
                st.switch_page("pages/home.py")
            else:
                st.error("❌ Invalid email or password.")

    st.markdown("<div style='text-align:center; margin-top:1rem; font-size:13px; color:#666;'>Don't have an account?</div>", unsafe_allow_html=True)

    if st.button("Sign Up", key="goto_signup", use_container_width=True):
        st.switch_page("pages/signup.py")