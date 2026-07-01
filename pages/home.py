import streamlit as st
import streamlit.components.v1 as components
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_connection

st.set_page_config(
    page_title="Home — ClinicBot",
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
    </style>
""", unsafe_allow_html=True)

if st.session_state.get("clinic") is None:
    st.switch_page("app.py")

clinic = st.session_state.clinic

# ── Load clinic info from DB ──
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

clinic_info = get_clinic_info(clinic["id"])

# ── Checklist logic ──
has_address   = bool(clinic_info and (clinic_info.get("address") or "").strip())
has_doctors   = bool(clinic_info and (clinic_info.get("doctors") or "").strip())
has_timings   = bool(clinic_info and (clinic_info.get("timings") or "").strip())
has_facilities = bool(clinic_info and (clinic_info.get("facilities") or "").strip())

def check(done):
    return '<div class="dot-done"></div>' if done else '<div class="dot-pending"></div>'

# ── Clinic info display ──
clinic_name_display    = clinic_info["clinic_name"] if clinic_info else clinic["clinic_name"]
address_display        = clinic_info["address"] if has_address else "Not set yet"
doctors_display        = clinic_info["doctors"].replace("\n", "<br>") if has_doctors else "Not set yet"
timings_display        = clinic_info["timings"].replace("\n", "<br>") if has_timings else "Not set yet"
facilities_display     = clinic_info["facilities"] if has_facilities else "Not set yet"

# ── Navbar ──
col1, col2, col3, col4, col5 = st.columns([5, 1, 1, 1, 1])
with col1:
    if st.button("ClinicBot", key="logo_btn"):
        st.switch_page("pages/home.py")
with col2:
    if st.button("Chatbot", key="chatbot_nav"):
        st.switch_page("pages/chatbot.py")
with col3:
    if st.button("Widget", key="widget_nav"):
        st.switch_page("pages/widget.py")
with col4:
    if st.button("Dashboard", key="dash_btn"):
        st.switch_page("pages/Dashboard.py")
with col5:
    if st.button("Logout", key="logout_btn"):
        st.session_state.clinic = None
        st.switch_page("app.py")

st.markdown("<hr style='border:none; border-top:0.5px solid #2a2a2a; margin:0;'>", unsafe_allow_html=True)

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0a0a0a;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #e8e6e1;
    overflow-x: hidden;
  }}
  .dot-bg {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    background-image: radial-gradient(circle, #2a2a2a 1px, transparent 1px);
    background-size: 28px 28px;
  }}
  .dot-glow {{
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(127,119,221,0.12) 0%, rgba(83,74,183,0.06) 40%, transparent 70%);
    z-index: 0;
    pointer-events: none;
  }}
  .content {{ position: relative; z-index: 1; }}

  .hero {{
    text-align: center;
    padding: 4rem 2rem 2rem;
    max-width: 700px;
    margin: 0 auto;
  }}
  .welcome-badge {{
    display: inline-block;
    background: #1a1a2e;
    border: 0.5px solid #534ab7;
    color: #afa9ec;
    font-size: 12px;
    padding: 4px 16px;
    border-radius: 20px;
    margin-bottom: 1.5rem;
  }}
  .hero h1 {{
    font-size: 42px;
    font-weight: 600;
    color: #fff;
    letter-spacing: -1px;
    line-height: 1.2;
    margin-bottom: 1rem;
  }}
  .hero h1 span {{ color: #7f77dd; }}
  .hero p {{ font-size: 15px; color: #666; line-height: 1.7; }}

  .stats {{
    display: flex;
    gap: 16px;
    justify-content: center;
    padding: 2rem 3rem;
    max-width: 900px;
    margin: 0 auto;
  }}
  .stat-card {{
    background: #111;
    border: 0.5px solid #222;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    flex: 1;
    transition: border-color 0.2s;
  }}
  .stat-card:hover {{ border-color: #534ab7; }}
  .stat-label {{ font-size: 12px; color: #555; margin-bottom: 6px; }}
  .stat-value {{ font-size: 28px; font-weight: 600; color: #fff; margin-bottom: 4px; }}
  .stat-sub {{ font-size: 11px; color: #534ab7; }}
  .stat-sub.green {{ color: #22c55e; }}

  .section {{
    max-width: 900px;
    margin: 0 auto;
    padding: 0 3rem 2rem;
  }}
  .section-title {{
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    margin-bottom: 1rem;
  }}

  /* Clinic Info */
  .info-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }}
  .info-card {{
    background: #111;
    border: 0.5px solid #222;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
  }}
  .info-label {{
    font-size: 11px;
    color: #555;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .info-value {{
    font-size: 13px;
    color: #e8e6e1;
    line-height: 1.6;
  }}
  .info-value.empty {{ color: #444; font-style: italic; }}

  /* Checklist */
  .setup-card {{
    background: #111;
    border: 0.5px solid #222;
    border-radius: 12px;
    padding: 1.4rem;
  }}
  .setup-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 0.5px solid #1a1a1a;
    font-size: 13px;
    color: #888;
  }}
  .setup-row:last-child {{ border-bottom: none; }}
  .dot-done {{ width: 8px; height: 8px; border-radius: 50%; background: #22c55e; flex-shrink: 0; }}
  .dot-pending {{ width: 8px; height: 8px; border-radius: 50%; background: #333; flex-shrink: 0; }}

  footer {{
    text-align: center;
    padding: 2rem;
    font-size: 12px;
    color: #333;
    border-top: 0.5px solid #111;
    margin-top: 2rem;
  }}
</style>
</head>
<body>

<div class="dot-bg"></div>
<div class="dot-glow"></div>

<div class="content">

  <!-- HERO -->
  <div class="hero">
    <div class="welcome-badge">👋 Welcome back, {clinic_name_display}</div>
    <h1>Your Clinic's AI<br><span>Command Center</span></h1>
    <p>Everything you need to manage your AI chatbot,<br>
       track patient interactions, and grow your clinic.</p>
  </div>

  <!-- STATS -->
  <div class="stats">
    <div class="stat-card">
      <div class="stat-label">Total Chats</div>
      <div class="stat-value">0</div>
      <div class="stat-sub">No chats yet</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Appointments</div>
      <div class="stat-value">0</div>
      <div class="stat-sub">No appointments yet</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Chatbot Status</div>
      <div class="stat-value">Active</div>
      <div class="stat-sub green">● Online</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Plan</div>
      <div class="stat-value" style="font-size:20px; padding-top:4px;">Basic</div>
      <div class="stat-sub">$19/month</div>
    </div>
  </div>

  <!-- CLINIC INFO -->
  <div class="section">
    <div class="section-title">🏥 Your Clinic Info</div>
    <div class="info-grid">
      <div class="info-card">
        <div class="info-label">Clinic Name</div>
        <div class="info-value">{clinic_name_display}</div>
      </div>
      <div class="info-card">
        <div class="info-label">Address</div>
        <div class="info-value {'empty' if not has_address else ''}">{address_display}</div>
      </div>
      <div class="info-card">
        <div class="info-label">Doctors & Staff</div>
        <div class="info-value {'empty' if not has_doctors else ''}">{doctors_display}</div>
      </div>
      <div class="info-card">
        <div class="info-label">Clinic Timings</div>
        <div class="info-value {'empty' if not has_timings else ''}">{timings_display}</div>
      </div>
      <div class="info-card" style="grid-column: span 2;">
        <div class="info-label">Facilities & Services</div>
        <div class="info-value {'empty' if not has_facilities else ''}">{facilities_display}</div>
      </div>
    </div>
  </div>

  <!-- SETUP CHECKLIST -->
  <div class="section">
    <div class="section-title">Setup Checklist</div>
    <div class="setup-card">
      <div class="setup-row">{check(True)} Account created</div>
      <div class="setup-row">{check(True)} Clinic name set</div>
      <div class="setup-row">{check(has_address)} Add clinic address</div>
      <div class="setup-row">{check(has_doctors)} Add doctors & staff</div>
      <div class="setup-row">{check(has_timings)} Add clinic timings</div>
      <div class="setup-row">{check(has_facilities)} Add clinic facilities</div>
    </div>
  </div>

  <footer>© 2025 ClinicBot — AI Chatbot for Clinics</footer>
</div>

</body>
</html>
""", height=1300, scrolling=False)