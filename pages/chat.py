import streamlit as st
import sys
import os
import requests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_connection

st.set_page_config(
    page_title="Clinic Chat",
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

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_MODEL   = "llama-3.3-70b-versatile"

# ── Get clinic ID from URL ──
params    = st.query_params
clinic_id = params.get("clinic", None)

# ── Load clinic info from DB ──
def get_clinic_by_id(clinic_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clinics WHERE id = ?", (clinic_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except:
        return None

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

# ── If no clinic ID show error ──
if not clinic_id:
    st.markdown("""
        <div style='text-align:center; padding:5rem 2rem;'>
            <div style='font-size:48px; margin-bottom:1rem;'>❌</div>
            <div style='font-size:20px; font-weight:600; color:#fff; margin-bottom:8px;'>
                Invalid Link
            </div>
            <div style='font-size:14px; color:#666;'>
                This chat link is invalid or expired.
                Please contact the clinic for a valid link.
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

clinic      = get_clinic_by_id(clinic_id)
clinic_info = get_clinic_info(clinic_id)

# ── If clinic not found ──
if not clinic:
    st.markdown("""
        <div style='text-align:center; padding:5rem 2rem;'>
            <div style='font-size:48px; margin-bottom:1rem;'>🏥</div>
            <div style='font-size:20px; font-weight:600; color:#fff; margin-bottom:8px;'>
                Clinic Not Found
            </div>
            <div style='font-size:14px; color:#666;'>
                This clinic does not exist in our system.
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

clinic_name = clinic_info["clinic_name"] if clinic_info else clinic["clinic_name"]
address     = (clinic_info.get("address") or "") if clinic_info else ""
doctors     = (clinic_info.get("doctors") or "") if clinic_info else ""
timings     = (clinic_info.get("timings") or "") if clinic_info else ""
facilities  = (clinic_info.get("facilities") or "") if clinic_info else ""

# ── Build system prompt ──
def build_system_prompt():
    return f"""You are a helpful AI receptionist for {clinic_name}, a medical clinic. Answer patient questions politely and accurately based ONLY on the clinic info below.

CLINIC INFORMATION:
- Clinic Name: {clinic_name}
- Address: {address if address else "Not provided"}
- Doctors & Staff: {doctors if doctors else "Not provided"}
- Clinic Timings: {timings if timings else "Not provided"}
- Facilities & Services: {facilities if facilities else "Not provided"}

IMPORTANT: Use the clinic info above to answer. If facilities are listed, tell the patient about them. Never say you don't have information if it is listed above.

RULES:
1. Only answer questions related to this clinic or general health queries.
2. Always be polite, professional and helpful.
3. If asked about something genuinely not in the clinic info, suggest calling the clinic.
4. Never make up info not listed above.
5. Keep answers short and clear.
6. If urgent medical help needed, advise visiting clinic or calling emergency services.
7. Answer in English or Urdu depending on what language the patient uses.

You represent {clinic_name}. Be warm like a receptionist."""

# ── Call Groq API ──
def ask_groq(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "system", "content": build_system_prompt()}] + messages,
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        data = response.json()
        if "error" in data:
            return "⚠️ Sorry I am having trouble right now. Please try again."
        return data["choices"][0]["message"]["content"]
    except:
        return "⚠️ Connection error. Please check your internet and try again."

# ── Get and store response ──
def get_and_store_response():
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            response = ask_groq(st.session_state.public_chat_messages)
        st.markdown(f"<div style='color:#c8c4f4;'>{response}</div>", unsafe_allow_html=True)
    st.session_state.public_chat_messages.append({"role": "assistant", "content": response})

# ── Page Header ──
st.markdown(f"""
    <div style='background:#111; border-bottom:0.5px solid #222; padding:1rem 2rem;
    display:flex; align-items:center; justify-content:space-between;'>
        <div>
            <div style='font-size:18px; font-weight:600; color:#fff;'>
                🏥 {clinic_name}
            </div>
            <div style='font-size:12px; color:#666; margin-top:2px;'>
                AI Receptionist • Powered by ClinicBot
            </div>
        </div>
        <div style='background:#1a1a2e; border:0.5px solid #534ab7;
        border-radius:20px; padding:4px 12px; font-size:11px; color:#afa9ec;'>
            🟢 Online
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Chat area ──
_, chat_col, _ = st.columns([1, 6, 1])

with chat_col:

    if "public_chat_messages" not in st.session_state:
        st.session_state.public_chat_messages = []

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Clinic info cards — ALWAYS VISIBLE ──
    st.markdown(f"""
        <div style='background:#111; border:0.5px solid #222; border-radius:12px;
        padding:1rem 1.5rem; margin-bottom:1rem;'>
            <div style='font-size:14px; font-weight:600; color:#fff; margin-bottom:0.8rem;'>
                🏥 {clinic_name}
            </div>
            <div style='display:grid; grid-template-columns:repeat(2,1fr); gap:10px;'>
                <div>
                    <div style='font-size:10px; color:#555; margin-bottom:3px;'>⏰ TIMINGS</div>
                    <div style='font-size:12px; color:#aaa;'>{timings if timings else "Not set yet"}</div>
                </div>
                <div>
                    <div style='font-size:10px; color:#555; margin-bottom:3px;'>📍 ADDRESS</div>
                    <div style='font-size:12px; color:#aaa;'>{address if address else "Not set yet"}</div>
                </div>
                <div>
                    <div style='font-size:10px; color:#555; margin-bottom:3px;'>👨‍⚕️ DOCTORS</div>
                    <div style='font-size:12px; color:#aaa;'>{doctors if doctors else "Not set yet"}</div>
                </div>
                <div>
                    <div style='font-size:10px; color:#555; margin-bottom:3px;'>🏥 FACILITIES</div>
                    <div style='font-size:12px; color:#aaa;'>{facilities if facilities else "Not set yet"}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Welcome + Suggested questions — only before first message ──
    if not st.session_state.public_chat_messages:
        st.markdown(f"""
            <div style='background:#111; border:0.5px solid #222; border-radius:12px;
            padding:1.5rem; text-align:center; margin-bottom:1rem;'>
                <div style='font-size:28px; margin-bottom:8px;'>👋</div>
                <div style='font-size:16px; font-weight:600; color:#fff; margin-bottom:6px;'>
                    Welcome to {clinic_name}
                </div>
                <div style='font-size:13px; color:#666;'>
                    Ask me anything about our clinic!
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size:12px; color:#555; margin-bottom:0.8rem;'>Suggested questions:</div>", unsafe_allow_html=True)
        q1, q2, q3 = st.columns(3)
        with q1:
            if st.button("⏰ Timings?", use_container_width=True, key="pq1"):
                st.session_state.public_chat_messages.append({"role": "user", "content": "What are your clinic timings?"})
                st.rerun()
        with q2:
            if st.button("👨‍⚕️ Doctors?", use_container_width=True, key="pq2"):
                st.session_state.public_chat_messages.append({"role": "user", "content": "Who are the doctors at your clinic?"})
                st.rerun()
        with q3:
            if st.button("🏥 Services?", use_container_width=True, key="pq3"):
                st.session_state.public_chat_messages.append({"role": "user", "content": "What services do you offer?"})
                st.rerun()

    # ── Clear button — only when messages exist ──
    if st.session_state.public_chat_messages:
        if st.button("🗑️ Clear Chat", key="clear_public"):
            st.session_state.public_chat_messages = []
            st.rerun()

    # ── Chat input ──
    user_input = st.chat_input("Ask anything about the clinic...")

    # ── Display messages ──
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.public_chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(
                    f"<div style='color: {'#e8e6e1' if msg['role'] == 'user' else '#c8c4f4'};'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )

        if (
            st.session_state.public_chat_messages
            and st.session_state.public_chat_messages[-1]["role"] == "user"
            and (
                len(st.session_state.public_chat_messages) == 1
                or st.session_state.public_chat_messages[-2]["role"] == "user"
            )
        ):
            get_and_store_response()
            st.rerun()

    # ── Handle manual input ──
    if user_input:
        st.session_state.public_chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"<div style='color:#e8e6e1;'>{user_input}</div>", unsafe_allow_html=True)
        get_and_store_response()
        st.rerun()

# ── Footer ──
st.markdown("""
    <div style='text-align:center; padding:1.5rem; font-size:12px; color:#333;
    border-top:0.5px solid #111; margin-top:2rem;'>
        Powered by <span style='color:#7f77dd;'>ClinicBot</span> — AI Chatbot for Clinics
    </div>
""", unsafe_allow_html=True)