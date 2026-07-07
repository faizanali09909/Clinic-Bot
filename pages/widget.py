import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Widget Code — ClinicBot",
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
        box-shadow: none !important;
    }
    .stButton button:hover {
        border-color: #7f77dd !important;
        color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.get("clinic") is None:
    st.switch_page("app.py")

clinic = st.session_state.clinic
clinic_id = clinic["id"]
clinic_name = clinic["clinic_name"]

# ── Your live Streamlit app base URL ──
APP_BASE_URL = "https://clinic-bot-d6vvszrnmmqkmzk6htype2.streamlit.app"

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
    if st.button("Dashboard", key="dash_nav"):
        st.switch_page("pages/Dashboard.py")
with col5:
    if st.button("Home", key="home_btn"):
        st.switch_page("pages/home.py")
with col6:
    if st.button("Logout", key="logout_btn"):
        st.session_state.clinic = None
        st.switch_page("app.py")

st.markdown("<hr style='border:none; border-top:0.5px solid #2a2a2a; margin:0 0 2rem 0;'>", unsafe_allow_html=True)

st.markdown("""
    <div style='padding: 0 3rem 1rem 3rem;'>
        <div style='font-size:24px; font-weight:600; color:#fff; margin-bottom:8px;'>
            🌐 Widget & Sharing
        </div>
        <div style='font-size:14px; color:#666;'>
            Share your clinic chatbot with patients.
        </div>
    </div>
""", unsafe_allow_html=True)

_, main_col, _ = st.columns([1, 6, 1])

with main_col:

    # ── Widget Code — Basic ✅ ──
    st.markdown("""
        <div style='background:#111; border:0.5px solid #222; border-radius:12px;
        padding:1.5rem; margin-bottom:1.5rem;'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:0.5rem;'>
                <div style='font-size:15px; font-weight:600; color:#fff;'>📋 Widget Code</div>
                <span style='background:#1a1a2e; border:0.5px solid #222; color:#666;
                font-size:10px; padding:2px 8px; border-radius:20px;'>✅ Basic</span>
            </div>
            <div style='font-size:13px; color:#666;'>
                Add this code just before the closing &lt;/body&gt; tag on your website.
            </div>
        </div>
    """, unsafe_allow_html=True)

    widget_code = f"""<!-- ClinicBot Widget -->
<script>
  window.clinicBotConfig = {{
    clinicId: "{clinic_id}",
    clinicName: "{clinic_name}"
  }};
</script>
<script src="{APP_BASE_URL}/widget.js"></script>"""

    st.code(widget_code, language="html")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Shareable Link — Basic ✅ ──
    shareable_link = f"{APP_BASE_URL}/chat?clinic={clinic_id}"

    st.markdown(f"""
        <div style='background:#111; border:0.5px solid #222; border-radius:12px;
        padding:1.5rem; margin-bottom:1.5rem;'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:0.8rem;'>
                <div style='font-size:15px; font-weight:600; color:#fff;'>🔗 Shareable Link</div>
                <span style='background:#1a1a2e; border:0.5px solid #222; color:#666;
                font-size:10px; padding:2px 8px; border-radius:20px;'>✅ Basic</span>
            </div>
            <div style='font-size:13px; color:#666; margin-bottom:1rem;'>
                Share this link on WhatsApp, Google Maps, Facebook, Instagram bio.
            </div>
            <div style='background:#1a1a1a; border:0.5px solid #2a2a2a; border-radius:8px;
            padding:10px 14px; font-size:13px; color:#7f77dd; font-family:monospace;'>
                {shareable_link}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── QR Code — Pro 🔒 ──
    st.markdown("""
        <div style='background:#0f0f1a; border:0.5px solid #534ab7;
        border-radius:12px; padding:1.5rem; margin-bottom:1.5rem; opacity:0.7;'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:0.8rem;'>
                <div style='font-size:15px; font-weight:600; color:#fff;'>📱 QR Code</div>
                <span style='background:#1a1a2e; border:0.5px solid #534ab7; color:#afa9ec;
                font-size:10px; padding:2px 8px; border-radius:20px;'>🔒 Pro</span>
            </div>
            <div style='font-size:13px; color:#666; margin-bottom:1rem;'>
                Generate a QR code for your clinic reception. Patients scan and chat instantly.
            </div>
            <div style='background:#111; border:0.5px solid #222; border-radius:8px;
            padding:2rem; text-align:center;'>
                <div style='font-size:32px; margin-bottom:8px;'>🔒</div>
                <div style='font-size:14px; color:#afa9ec; font-weight:600;
                margin-bottom:6px;'>Pro Feature</div>
                <div style='font-size:12px; color:#555;'>
                    Upgrade to Pro to generate and download your clinic QR code.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── How to use shareable link ──
    st.markdown("""
        <div style='background:#111; border:0.5px solid #222; border-radius:12px; padding:1.5rem;'>
            <div style='font-size:15px; font-weight:600; color:#fff; margin-bottom:1rem;'>
                📖 Where to share your link
            </div>
            <div style='font-size:13px; color:#888; line-height:2;'>
                <b style='color:#e8e6e1;'>Google Maps</b> — Add in your business website/description<br>
                <b style='color:#e8e6e1;'>WhatsApp Business</b> — Add in your bio or auto-reply<br>
                <b style='color:#e8e6e1;'>Facebook</b> — Add in your page about section<br>
                <b style='color:#e8e6e1;'>Instagram</b> — Add in your bio link<br>
                <b style='color:#e8e6e1;'>Website</b> — Paste the widget code instead
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align:center; padding:2rem; font-size:13px; color:#444;
    border-top:0.5px solid #1a1a1a; margin-top:3rem;'>
        © 2025 ClinicBot — AI Chatbot for Clinics
    </div>
""", unsafe_allow_html=True)