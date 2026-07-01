import os

# ── Use /tmp on Streamlit Cloud ──
if os.path.exists("/mount/src"):
    DB_PATH = "/tmp/clinicbot.db"
else:
    DB_PATH = "clinicbot.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clinics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clinic_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            plan TEXT DEFAULT 'basic',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_clinic(clinic_name, email, password, plan="basic"):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clinics (clinic_name, email, password, plan) VALUES (?, ?, ?, ?)",
            (clinic_name, email, hash_password(password), plan)
        )
        conn.commit()
        clinic_id = cursor.lastrowid
        conn.close()
        return {"id": clinic_id, "clinic_name": clinic_name, "email": email, "plan": plan}
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_clinic_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clinics WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def login_clinic(email, password):
    clinic = get_clinic_by_email(email)
    if clinic and clinic["password"] == hash_password(password):
        return clinic
    return None

def get_plan(clinic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT plan FROM clinics WHERE id = ?", (clinic_id,))
    row = cursor.fetchone()
    conn.close()
    return row["plan"] if row else "basic"

def update_plan(clinic_id, plan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clinics SET plan = ? WHERE id = ?", (plan, clinic_id))
    conn.commit()
    conn.close()

init_db()