import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import create_clinic, get_clinic_by_email

st.set_page_config(
    page_title="Sign Up — ClinicBot",
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
    .stTextInput input:-webkit-autofill {
        -webkit-box-shadow: 0 0 0px 1000px #1a1a1a inset !important;
        -webkit-text-fill-color: #e8e6e1 !important;
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

# ── Read plan from session state ──
selected_plan = st.session_state.get("selected_plan", "basic").lower()
if selected_plan not in ["basic", "pro", "premium"]:
    selected_plan = "basic"

# ── Plan display info ──
plan_info = {
    "basic":   {"label": "Basic",   "price": "$19/month", "color": "#666",   "border": "#333"},
    "pro":     {"label": "Pro",     "price": "$49/month", "color": "#7f77dd","border": "#534ab7"},
    "premium": {"label": "Premium", "price": "$99/month", "color": "#afa9ec","border": "#534ab7"},
}
plan = plan_info[selected_plan]

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
            <span style='font-size:22px; font-weight:600; color:#fff;'>Create your account</span>
        </div>
        <div style='text-align:center; font-size:13px; color:#666; margin-bottom:1rem;'>
            Start automating your clinic today
        </div>
    """, unsafe_allow_html=True)

    # ── Show selected plan badge ──
    st.markdown(f"""
        <div style='background:#0f0f1a; border:0.5px solid {plan["border"]};
        border-radius:8px; padding:10px 14px; margin-bottom:1.5rem; text-align:center;'>
            <span style='font-size:12px; color:#888;'>Selected Plan: </span>
            <span style='font-size:13px; font-weight:600; color:{plan["color"]};'>
                {plan["label"]} — {plan["price"]}
            </span>
            &nbsp;
            <a href='/' style='font-size:11px; color:#555; text-decoration:underline;'>
                Change plan
            </a>
        </div>
    """, unsafe_allow_html=True)

    clinic_name = st.text_input("Clinic Name", placeholder="e.g. City Health Clinic")
    address     = st.text_input("Clinic Address", placeholder="e.g. 123 Main Street, Faisalabad")
    email       = st.text_input("Email Address", placeholder="you@clinic.com")
    password    = st.text_input("Password", placeholder="Min. 6 characters", type="password")
    confirm     = st.text_input("Confirm Password", placeholder="Repeat your password", type="password")

    if st.button(f"Create {plan['label']} Account →", use_container_width=True, key="signup_btn"):
        if not clinic_name or not address or not email or not password or not confirm:
            st.error("❌ All fields are required.")
        elif password != confirm:
            st.error("❌ Passwords do not match.")
        elif len(password) < 6:
            st.error("❌ Password must be at least 6 characters.")
        elif get_clinic_by_email(email):
            st.error("❌ An account with this email already exists.")
        else:
            clinic = create_clinic(clinic_name, email, password, selected_plan)
            if clinic:
                try:
                    from database import get_connection
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS clinic_info (
                            clinic_id INTEGER PRIMARY KEY,
                            clinic_name TEXT,
                            doctors TEXT,
                            timings TEXT,
                            facilities TEXT,
                            address TEXT
                        )
                    """)
                    cursor.execute("""
                        INSERT INTO clinic_info (clinic_id, clinic_name, address)
                        VALUES (?, ?, ?)
                        ON CONFLICT(clinic_id) DO UPDATE SET
                            clinic_name = excluded.clinic_name,
                            address = excluded.address
                    """, (clinic["id"], clinic_name, address))
                    conn.commit()
                    conn.close()
                except Exception as e:
                    print(f"Error saving address: {e}")

                st.session_state.clinic = clinic
                st.session_state["selected_plan"] = selected_plan
                st.switch_page("pages/home.py")
            else:
                st.error("❌ Something went wrong. Please try again.")

    st.markdown("<div style='text-align:center; margin-top:1rem; font-size:13px; color:#666;'>Already have an account?</div>", unsafe_allow_html=True)

    if st.button("Login", key="goto_login", use_container_width=True):
        st.switch_page("pages/login.py")