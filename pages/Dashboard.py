import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_connection

st.set_page_config(
    page_title="Dashboard — ClinicBot",
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

    .stButton button {
        background: transparent !important;
        border: 0.5px solid #333 !important;
        color: #ccc !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 400 !important;
    }
    .stButton button:hover {
        border-color: #7f77dd !important;
        color: #fff !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: #1a1a1a !important;
        border: 0.5px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #e8e6e1 !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #7f77dd !important;
    }
    .stTextInput input:disabled {
        background: #111 !important;
        color: #444 !important;
        cursor: not-allowed !important;
    }
    .stTextInput label, .stTextArea label {
        color: #aaa !important;
        font-size: 13px !important;
    }

    /* Save button purple */
    div[data-testid="column"]:nth-child(1) .stButton button {
        background: #7f77dd !important;
        border: none !important;
        color: #fff !important;
        font-weight: 600 !important;
    }
    div[data-testid="column"]:nth-child(1) .stButton button:hover {
        background: #6d65cc !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.get("clinic") is None:
    st.switch_page("app.py")

clinic = st.session_state.clinic

def get_clinic_info(clinic_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clinic_info WHERE clinic_id = ?", (clinic_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except:
        return None

def save_clinic_info(clinic_id, clinic_name, doctors, timings, facilities, address):
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
        INSERT INTO clinic_info (clinic_id, clinic_name, doctors, timings, facilities, address)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(clinic_id) DO UPDATE SET
            clinic_name = excluded.clinic_name,
            doctors = excluded.doctors,
            timings = excluded.timings,
            facilities = excluded.facilities,
            address = excluded.address
    """, (clinic_id, clinic_name, doctors, timings, facilities, address))
    conn.commit()
    conn.close()

clinic_info = get_clinic_info(clinic["id"])

# ── Navbar ──
col1, col2, col3, col4, col5, col6 = st.columns([4, 1, 1, 1, 1, 1])
with col1:
    if st.button("ClinicBot", key="logo_btn"):
        st.switch_page("pages/home.py")
with col2:
    st.markdown(f"<div style='padding:14px 0; font-size:12px; color:#888; text-align:center;'>{clinic['clinic_name']}</div>", unsafe_allow_html=True)
with col3:
    if st.button("Chatbot", key="chatbot_nav"):
        st.switch_page("pages/chatbot.py")
with col4:
    if st.button("Widget", key="widget_nav"):
        st.switch_page("pages/widget.py")
with col5:
    if st.button("Home", key="home_nav"):
        st.switch_page("pages/home.py")
with col6:
    if st.button("Logout", key="logout"):
        st.session_state.clinic = None
        st.switch_page("app.py")

st.markdown("<hr style='border:none; border-top:0.5px solid #2a2a2a; margin:0 0 2rem 0;'>", unsafe_allow_html=True)

# ── Page Title ──
st.markdown("""
    <div style='padding: 0.5rem 3rem 1.5rem 3rem;'>
        <div style='font-size:22px; font-weight:600; color:#fff; margin-bottom:6px;'>
            🏥 Clinic Setup
        </div>
        <div style='font-size:14px; color:#666;'>
            Fill in your clinic details so your AI chatbot can answer patient questions correctly.
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Pro locked badge ──
def pro_badge():
    return "<span style='background:#1a1a2e; border:0.5px solid #534ab7; color:#afa9ec; font-size:10px; padding:2px 8px; border-radius:20px; margin-left:8px;'>🔒 Pro</span>"

# ── Form fields ──
st.markdown(f"<div style='padding: 0 3rem;'><div style='font-size:13px; color:#aaa; margin-bottom:0.5rem;'>Clinic Name {pro_badge()} <span style='color:#555; font-size:12px;'> — Upgrade to Pro to change</span></div></div>", unsafe_allow_html=True)

_, c1, c2, c3 = st.columns([0.15, 2, 2, 2])

with c1:
    # Clinic Name — LOCKED for Basic
    st.text_input(
        "Clinic Name 🔒",
        value=clinic_info["clinic_name"] if clinic_info else clinic["clinic_name"],
        disabled=True,
        key="clinic_name_locked"
    )

with c2:
    # Address — LOCKED for Basic
    st.text_input(
        "Clinic Address 🔒",
        value=clinic_info["address"] if clinic_info else "",
        disabled=True,
        key="address_locked"
    )

with c3:
    st.markdown("""
        <div style='background:#0f0f1a; border:0.5px solid #534ab7;
        border-radius:8px; padding:10px 14px; margin-top:28px;'>
            <div style='font-size:12px; color:#afa9ec;'>
                🔒 Clinic Name & Address editing is a
                <b style='color:#7f77dd;'>Pro feature</b>.
                Upgrade to change these.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div style='padding: 0 3rem;'>", unsafe_allow_html=True)
st.markdown("<div style='font-size:14px; color:#aaa; margin-bottom:0.5rem;'>Editable Info <span style='background:#1a1a2e; border:0.5px solid #222; color:#666; font-size:10px; padding:2px 8px; border-radius:20px; margin-left:8px;'>✅ Basic</span></div>", unsafe_allow_html=True)

e1, e2, e3 = st.columns(3)

with e1:
    timings_input = st.text_input(
        "Clinic Timings",
        value=clinic_info["timings"] if clinic_info else "",
        placeholder="e.g. Mon-Sat: 9am-6pm"
    )

with e2:
    doctors_input = st.text_input(
        "Doctors / Staff",
        value=clinic_info["doctors"] if clinic_info else "",
        placeholder="e.g. Dr. Ahmed"
    )

with e3:
    facilities_input = st.text_input(
        "Facilities & Services",
        value=clinic_info["facilities"] if clinic_info else "",
        placeholder="e.g. X-Ray, Lab Tests"
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Save Button ──
save_col, _, _ = st.columns([2, 4, 4])
with save_col:
    if st.button("💾  Save Clinic Info", use_container_width=True, key="save_btn"):
        if not timings_input and not doctors_input and not facilities_input:
            st.error("❌ Please fill in at least one field.")
        else:
            save_clinic_info(
                clinic["id"],
                clinic_info["clinic_name"] if clinic_info else clinic["clinic_name"],
                doctors_input,
                timings_input,
                facilities_input,
                clinic_info["address"] if clinic_info else ""
            )
            st.success("✅ Clinic info saved successfully!")

# ── Footer ──
st.markdown("""
    <div style='text-align:center; padding:2rem; font-size:13px; color:#444;
    border-top:0.5px solid #1a1a1a; margin-top:3rem;'>
        © 2025 ClinicBot — AI Chatbot for Clinics
    </div>
""", unsafe_allow_html=True)