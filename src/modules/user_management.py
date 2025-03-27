import streamlit as st
from metadata_management import cursor, conn

def check_login(username, password):
    """
    Gibt die Rolle zurück, falls Login korrekt, sonst None.
    """
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

def ensure_default_users():
    """
    Legt zwei Default-Nutzer an, falls sie noch nicht existieren.
    """
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("Verwaltung", "Passwort", "Verwaltung"))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("Bürger", "Passwort", "Bürger"))
    conn.commit()

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Benutzername")
    password = st.sidebar.text_input("Passwort", type="password")
    if st.sidebar.button("Anmelden"):
        role = check_login(username, password)
        if role:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.success(f"Erfolgreich angemeldet als {username} (Rolle: {role})")
            st.rerun()
        else:
            st.error("Login fehlgeschlagen")

def logout():
    if st.sidebar.button("Abmelden"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None
        st.rerun()