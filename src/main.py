import streamlit as st
from db.connection import init_db
from modules.user_management import login, logout, ensure_default_users
from modules.antrag_logic import buerger_view
from modules.verwaltung_logic import verwaltung_view

def main():
    st.title("Mehrstufiges Antragsverfahren mit mehreren Anträgen")

    # Initialisierung der DB
    init_db()
    ensure_default_users()

    # Login-Check
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login()
        return

    # Logout
    logout()

    # Rolle
    role = st.session_state["role"]
    st.sidebar.write(f"Angemeldet als: **{st.session_state['username']}** (Rolle: {role})")

    if role == "Bürger":
        buerger_view()
    elif role == "Verwaltung":
        verwaltung_view()
    else:
        st.error("Unbekannte Rolle. Bitte wenden Sie sich an den Support.")

if __name__ == "__main__":
    main()