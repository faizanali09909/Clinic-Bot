import streamlit as st
import sys
import os
import requests
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_connection

st.set_page_config(
    page_title="Chatbot — ClinicBot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
    * { outline: none !important; box-shadow: none !important; }
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testbed="collapsedControl"] {display: none;}
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

    .stChatInput textarea {
        background: #1a1a1a !important;
        border: 0.5px solid #2a2a2a !important;
        border-radius: 12px !important;
        color: #e8e6e1 !important;
        font-size: 14px !important;
    }
    .stChatInput textarea:focus {
        border-color: #7f77dd !important;
    }

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.get("clinic") is None:
    st.switch_page("app.py")

clinic = st.session_state.clinic

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_MODEL   = "llama-3.3-70b-versatile"

# ── Load clinic info ──
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

# ── Build system prompt ──
def build_system_prompt(clinic, clinic_info):
    name       = clinic_info["clinic_name"] if clinic_info else clinic["clinic_name"]
    address    = clinic_info["address"]     if clinic_info and clinic_info.get("address")    else "Not provided"
    doctors    = clinic_info["doctors"]     if clinic_info and clinic_info.get("doctors")    else "Not provided"
    timings    = clinic_info["timings"]     if clinic_info and clinic_info.get("timings")    else "Not provided"
    facilities = clinic_info["facilities"] if clinic_info and clinic_info.get("facilities") else "Not provided"

    return f"""You are a helpful AI assistant for {name}, a medical clinic. Your job is to answer patient questions politely and accurately based on the clinic information below.

CLINIC INFORMATION:
- Clinic Name: {name}
- Address: {address}
- Doctors & Staff: {doctors}
- Clinic Timings: {timings}
- Facilities & Services: {facilities}

RULES:
1. Only answer questions related to this clinic or general health queries.
2. Always be polite, professional and helpful.
3. If asked about something not in the clinic info, say you don't have that information and suggest calling the clinic.
4. Never make up doctor names, prices or services that are not listed above.
5. Keep answers short and clear.
6. If a patient seems to need urgent medical help, always advise them to visit the clinic or call emergency services immediately.
7. You can answer in English or Urdu depending on what language the patient uses.

You represent {name}. Be warm and helpful like a receptionist."""

# ── Call Groq API ──
def ask_groq(messages, system_prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        data = response.json()

        if "error" in data:
            error_msg  = data["error"].get("message", "Unknown API error")
            error_type = data["error"].get("type", "")
            if "invalid_api_key" in error_type or "auth" in error_type.lower():
                return "⚠️ API key is invalid or expired. Please update the Groq API key."
            return f"⚠️ API Error: {error_msg}"

        if "choices" not in data or not data["choices"]:
            return "⚠️ Unexpected response from the AI service. Please try again."

        choice = data["choices"][0]
        if "message" not in choice or "content" not in choice["message"]:
            return "⚠️ Incomplete response received. Please try again."

        return choice["message"]["content"]

    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Please check your connection and try again."
    except requests.exceptions.ConnectionError:
        return "⚠️ Connection error. Please check your internet connection."
    except requests.exceptions.HTTPError as e:
        return f"⚠️ HTTP error occurred: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# ── Helper to get AI response and append to history ──
def get_and_store_response():
    system_prompt = build_system_prompt(clinic, clinic_info)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_groq(st.session_state.chat_messages, system_prompt)
        st.markdown(f"<div style='color:#c8c4f4;'>{response}</div>", unsafe_allow_html=True)
    st.session_state.chat_messages.append({"role": "assistant", "content": response})

# ── Navbar ──
col1, col2, col3, col4, col5, col6 = st.columns([4, 1, 1, 1, 1, 1])
with col1:
    if st.button("ClinicBot", key="logo_btn"):
        st.switch_page("pages/home.py")
with col2:
    st.markdown(f"<div style='padding:14px 0; font-size:12px; color:#888; text-align:center;'>{clinic['clinic_name']}</div>", unsafe_allow_html=True)
with col3:
    if st.button("Widget", key="widget_nav"):
        st.switch_page("pages/widget.py")
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

st.markdown("<hr style='border:none; border-top:0.5px solid #2a2a2a; margin:0;'>", unsafe_allow_html=True)

# ── Page Header ──
st.markdown(f"""
    <div style='padding: 1.5rem 3rem 0.5rem 3rem;'>
        <div style='font-size:22px; font-weight:600; color:#fff; margin-bottom:4px;'>
            🤖 AI Chatbot
        </div>
        <div style='font-size:13px; color:#666;'>
            Powered by {clinic_info["clinic_name"] if clinic_info else clinic["clinic_name"]} • Ask anything about the clinic
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Chat Layout ──
_, chat_col, _ = st.columns([1, 6, 1])

with chat_col:

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Clear chat button
    clear_col, _ = st.columns([1, 5])
    with clear_col:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Welcome + Suggested Questions (only when no messages) ──
    if not st.session_state.chat_messages:
        clinic_display_name = clinic_info["clinic_name"] if clinic_info else clinic["clinic_name"]
        st.markdown(f"""
            <div style='background:#111; border:0.5px solid #222; border-radius:12px;
            padding:1.5rem; text-align:center; margin-bottom:1.5rem;'>
                <div style='font-size:24px; margin-bottom:10px;'>👋</div>
                <div style='font-size:16px; font-weight:600; color:#fff; margin-bottom:6px;'>
                    Welcome to {clinic_display_name}
                </div>
                <div style='font-size:13px; color:#666;'>
                    Ask me anything about our clinic — timings, doctors, services and more!
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size:12px; color:#555; margin-bottom:0.8rem;'>Suggested questions:</div>", unsafe_allow_html=True)

        q1, q2, q3 = st.columns(3)
        with q1:
            if st.button("⏰ What are your timings?", use_container_width=True, key="suggest_q1"):
                st.session_state.chat_messages.append({"role": "user", "content": "What are your clinic timings?"})
                st.rerun()
        with q2:
            if st.button("👨‍⚕️ Who are your doctors?", use_container_width=True, key="suggest_q2"):
                st.session_state.chat_messages.append({"role": "user", "content": "Who are the doctors at your clinic?"})
                st.rerun()
        with q3:
            if st.button("🏥 What services do you offer?", use_container_width=True, key="suggest_q3"):
                st.session_state.chat_messages.append({"role": "user", "content": "What services and facilities do you offer?"})
                st.rerun()

    # ── Chat input pinned to bottom ──
    user_input = st.chat_input("Ask anything about the clinic...")

    # ── Display chat history ──
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(f"<div style='color: {'#e8e6e1' if msg['role'] == 'user' else '#c8c4f4'};'>{msg['content']}</div>", unsafe_allow_html=True)

        # ✅ Auto-respond to suggested question button clicks
        if (
            st.session_state.chat_messages
            and st.session_state.chat_messages[-1]["role"] == "user"
            and (
                len(st.session_state.chat_messages) == 1
                or st.session_state.chat_messages[-2]["role"] == "user"
            )
        ):
            get_and_store_response()
            st.rerun()

    # ── Handle manual chat input ──
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"<div style='color:#e8e6e1;'>{user_input}</div>", unsafe_allow_html=True)
        get_and_store_response()
        st.rerun()

# ── Footer ──
st.markdown("""
    <div style='text-align:center; padding:2rem; font-size:13px; color:#444;
    border-top:0.5px solid #1a1a1a; margin-top:2rem;'>
        © 2025 ClinicBot — AI Chatbot for Clinics
    </div>
""", unsafe_allow_html=True)