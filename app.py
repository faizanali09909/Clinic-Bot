import streamlit as st
import streamlit.components.v1 as components



st.set_page_config(
    page_title="ClinicBot",
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
    #root > div:first-child {background: #0a0a0a;}
    .stApp {background: #0a0a0a !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    footer {display: none;}

    [data-testid="column"] {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    [data-testid="stVerticalBlock"] {
        border: none !important;
        box-shadow: none !important;
        gap: 0 !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        border: none !important;
        box-shadow: none !important;
    }

    .stButton button {
        background: transparent !important;
        border: 0.5px solid #333 !important;
        color: #ccc !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        padding: 6px 18px !important;
        box-shadow: none !important;
        margin-top: 8px !important;
    }
    .stButton button:hover {
        border-color: #7f77dd !important;
        color: #fff !important;
        background: transparent !important;
    }
    div[data-testid="column"]:nth-child(3) .stButton button {
        background: #7f77dd !important;
        border: none !important;
        color: #fff !important;
        font-weight: 600 !important;
    }
    div[data-testid="column"]:nth-child(3) .stButton button:hover {
        background: #6d65cc !important;
        border: none !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton button {
        background: transparent !important;
        border: 0.5px solid #333 !important;
        color: #ccc !important;
        font-weight: 400 !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton button:hover {
        border-color: #7f77dd !important;
        color: #fff !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

if "clinic" not in st.session_state:
    st.session_state.clinic = None

if "selected_plan" not in st.session_state:
    st.session_state["selected_plan"] = "basic"

if st.session_state.clinic is not None:
    st.switch_page("pages/home.py")

# ── Navbar ──
col1, col2, col3, col4 = st.columns([7, 1, 1, 0.3])
with col1:
    st.markdown("<div style='padding:14px 0 14px 24px; font-size:20px; font-weight:600; color:#fff;'><span style='color:#7f77dd'>Clinic</span>Bot</div>", unsafe_allow_html=True)
with col2:
    if st.button("Login", key="nav_login", use_container_width=True):
        try:
            st.switch_page("pages/login.py")
        except:
            st.switch_page("login.py")
with col3:
    if st.button("Sign Up", key="nav_signup", use_container_width=True):
        st.session_state["selected_plan"] = "basic"
        try:
            st.switch_page("pages/signup.py")
        except:
            st.switch_page("signup.py")
with col4:
    st.markdown("")

st.markdown("<hr style='border:none; border-top:0.5px solid #2a2a2a; margin:0;'>", unsafe_allow_html=True)

# ── Hero + Features ──
components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0a0a0a;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #e8e6e1;
  }
  .hero {
    text-align: center;
    padding: 4rem 2rem 3rem;
    max-width: 720px;
    margin: 0 auto;
  }
  .badge {
    display: inline-block;
    background: #1a1a2e;
    border: 0.5px solid #534ab7;
    color: #afa9ec;
    font-size: 12px;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1.5rem;
  }
  h1 {
    font-size: 48px;
    font-weight: 600;
    line-height: 1.15;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 1.2rem;
  }
  h1 span { color: #7f77dd; }
  .hero p { font-size: 16px; color: #888; line-height: 1.7; }
  hr { border: none; border-top: 0.5px solid #1a1a1a; margin: 0 3rem; }
  .section { padding: 3rem; max-width: 1000px; margin: 0 auto; }
  h2 {
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    color: #fff;
    margin-bottom: 2rem;
  }
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
  .card {
    background: #111;
    border: 0.5px solid #222;
    border-radius: 12px;
    padding: 1.4rem;
    transition: border-color 0.2s;
  }
  .card:hover { border-color: #534ab7; }
  .card-icon { font-size: 28px; margin-bottom: 1rem; }
  .card h3 { font-size: 15px; font-weight: 600; color: #e8e6e1; margin-bottom: 6px; }
  .card p { font-size: 13px; color: #666; line-height: 1.6; }
</style>
</head>
<body>

<div class="hero">
  <div class="badge">AI-Powered • 24/7 Automated</div>
  <h1>AI Chatbot for<br><span>Your Clinic</span></h1>
  <p>Automate patient questions, bookings, and more.<br>
     Set up in 5 minutes. No coding required.</p>
</div>

<hr>

<div class="section">
  <h2>Everything your clinic needs</h2>
  <div class="grid-3">
    <div class="card"><div class="card-icon">⚡</div><h3>Setup in 5 minutes</h3><p>Fill your clinic info and get a working chatbot instantly.</p></div>
    <div class="card"><div class="card-icon">🤖</div><h3>AI powered answers</h3><p>Groq AI answers patient questions 24/7 automatically.</p></div>
    <div class="card"><div class="card-icon">💰</div><h3>Save money</h3><p>Cut receptionist costs with full automation.</p></div>
    <div class="card"><div class="card-icon">🌐</div><h3>Embed anywhere</h3><p>One line of code to add chatbot to any website.</p></div>
    <div class="card"><div class="card-icon">🔗</div><h3>Shareable link</h3><p>Share on WhatsApp, Google Maps, Facebook instantly.</p></div>
    <div class="card"><div class="card-icon">🔒</div><h3>Secure & private</h3><p>All data encrypted. Patient privacy guaranteed.</p></div>
  </div>
</div>

</body>
</html>
""", height=850, scrolling=False)

# ── Pricing ──
st.markdown("<hr style='border:none; border-top:0.5px solid #1a1a1a; margin:0 3rem;'>", unsafe_allow_html=True)

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0a0a0a;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #e8e6e1;
  }
  .pricing-section {
    padding: 2rem 3rem 3rem;
    max-width: 1000px;
    margin: 0 auto;
  }
  h2 {
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    color: #fff;
    margin-bottom: 2rem;
  }
  .pricing-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
  .card {
    position: relative;
    background: #111;
    border-radius: 12px;
    padding: 1.5rem;
    height: 420px;
    overflow: hidden;
    cursor: default;
    border: 1px solid transparent;
    transition: border-color 0.3s ease;
  }
  .card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    background-image: radial-gradient(circle, #2e2e2e 1px, transparent 1px);
    background-size: 22px 22px;
    opacity: 0;
    transition: opacity 0.35s ease;
    pointer-events: none;
    z-index: 0;
  }
  .card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    background: radial-gradient(ellipse at 50% 0%, rgba(127,119,221,0.12) 0%, transparent 65%);
    opacity: 0;
    transition: opacity 0.35s ease;
    pointer-events: none;
    z-index: 0;
  }
  .card:hover::before { opacity: 1; }
  .card:hover::after  { opacity: 1; }
  .card:hover { border-color: #534ab7; }
  .card.pro { border-color: #534ab7 !important; }
  .card.pro::before { opacity: 0 !important; }
  .card.pro:hover::before { opacity: 1 !important; }
  .card.pro::after { opacity: 0 !important; }
  .card.pro:hover::after { opacity: 1 !important; }
  .card-content { position: relative; z-index: 1; }
  .badge {
    display: inline-block;
    background: #1a1a2e;
    border: 0.5px solid #534ab7;
    color: #afa9ec;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
  }
  .plan-name { font-size: 15px; font-weight: 600; color: #fff; margin-bottom: 10px; }
  .price { font-size: 36px; font-weight: 600; color: #fff; margin-bottom: 4px; }
  .price span { font-size: 14px; color: #666; font-weight: 400; }
  ul { list-style: none; margin: 1rem 0 0; padding: 0; }
  li { font-size: 13px; color: #888; padding: 5px 0; }
  li.off { color: #444; }
</style>
</head>
<body>

<div class="pricing-section">
  <h2>Simple pricing</h2>
  <div class="pricing-grid">

    <div class="card">
      <div class="card-content">
        <div class="plan-name">Basic</div>
        <div class="price">$19<span>/month</span></div>
        <ul>
          <li>✓ &nbsp;AI Chatbot</li>
          <li>✓ &nbsp;FAQ answers</li>
          <li>✓ &nbsp;Widget code</li>
          <li>✓ &nbsp;Shareable link</li>
          <li>✓ &nbsp;Edit timings &amp; doctors</li>
          <li class="off">✗ &nbsp;Change clinic name</li>
          <li class="off">✗ &nbsp;Change clinic address</li>
          <li class="off">✗ &nbsp;QR Code</li>
        </ul>
      </div>
    </div>

    <div class="card pro">
      <div class="card-content">
        <div class="badge">Most popular</div>
        <div class="plan-name">Pro</div>
        <div class="price">$49<span>/month</span></div>
        <ul>
          <li>✓ &nbsp;Everything in Basic</li>
          <li>✓ &nbsp;Change clinic name</li>
          <li>✓ &nbsp;Change clinic address</li>
          <li>✓ &nbsp;QR Code generation</li>
          <li>✓ &nbsp;Appointment booking</li>
          <li>✓ &nbsp;WhatsApp integration</li>
          <li>✓ &nbsp;Priority support</li>
        </ul>
      </div>
    </div>

    <div class="card">
      <div class="card-content">
        <div class="plan-name">Premium</div>
        <div class="price">$99<span>/month</span></div>
        <ul>
          <li>✓ &nbsp;Everything in Pro</li>
          <li>✓ &nbsp;Analytics dashboard</li>
          <li>✓ &nbsp;Custom AI training</li>
          <li>✓ &nbsp;Dedicated support</li>
        </ul>
      </div>
    </div>

  </div>
</div>

</body>
</html>
""", height=520, scrolling=False)

# ── Pricing Buttons ──
_, b1, b2, b3, _ = st.columns([0.5, 1, 1, 1, 0.5])
with b1:
    if st.button("Sign Up — Basic", use_container_width=True, key="plan_basic"):
        st.session_state["selected_plan"] = "basic"
        try:
            st.switch_page("pages/signup.py")
        except:
            st.switch_page("signup.py")
with b2:
    if st.button("Sign Up — Pro", use_container_width=True, key="plan_pro"):
        st.session_state["selected_plan"] = "pro"
        try:
            st.switch_page("pages/signup.py")
        except:
            st.switch_page("signup.py")
with b3:
    if st.button("Sign Up — Premium", use_container_width=True, key="plan_premium"):
        st.session_state["selected_plan"] = "premium"
        try:
            st.switch_page("pages/signup.py")
        except:
            st.switch_page("signup.py")

st.markdown("""
    <div style='text-align:center; padding:2rem; font-size:13px; color:#444;
    border-top:0.5px solid #1a1a1a; margin-top:2rem;'>
        © 2025 ClinicBot — AI Chatbot for Clinics
    </div>
""", unsafe_allow_html=True)