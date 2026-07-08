import hashlib
import streamlit as st
from supabase import create_client, Client

# ── Supabase connection ──
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_clinic(clinic_name, email, password, plan="basic"):
    try:
        result = supabase.table("clinics").insert({
            "clinic_name": clinic_name,
            "email": email,
            "password": hash_password(password),
            "plan": plan
        }).execute()
        if result.data:
            clinic = result.data[0]
            return {"id": clinic["id"], "clinic_name": clinic["clinic_name"],
                    "email": clinic["email"], "plan": clinic["plan"]}
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_clinic_by_email(email):
    try:
        result = supabase.table("clinics").select("*").eq("email", email).execute()
        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def login_clinic(email, password):
    clinic = get_clinic_by_email(email)
    if clinic and clinic["password"] == hash_password(password):
        return clinic
    return None

def get_plan(clinic_id):
    try:
        result = supabase.table("clinics").select("plan").eq("id", clinic_id).execute()
        if result.data:
            return result.data[0]["plan"]
        return "basic"
    except:
        return "basic"

def update_plan(clinic_id, plan):
    try:
        supabase.table("clinics").update({"plan": plan}).eq("id", clinic_id).execute()
    except Exception as e:
        print(f"Error: {e}")

def get_connection():
    return supabase