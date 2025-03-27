import streamlit as st
from tinydb import Query

from src.db.connection import tiny_db, conn, cursor
from metadata_management import get_metadata, update_metadata
from src.modules.forms import load_config, render_fields, convert_dates
import datetime

def current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

def verwaltung_view():
    st.header("Verwaltungssicht")
    # Zeige alle vorhandenen Anträge
    cursor.execute("SELECT doc_key, owner FROM metadata")
    rows = cursor.fetchall()

    if not rows:
        st.info("Es liegen noch keine Anträge vor.")
        return

    # Selectbox mit allen Anträgen (doc_key + Besitzer)
    options = [f"{r[0]} (Besitzer: {r[1]})" for r in rows]
    selected = st.selectbox("Wähle einen Antrag aus", options)
    if selected:
        doc_key = selected.split(" ")[0]

        # Button zum Löschen des Antrags
        if st.button("Diesen Antrag löschen"):
            tiny_db.remove(Query().doc_key == doc_key)
            cursor.execute("DELETE FROM metadata WHERE doc_key=?", (doc_key,))
            conn.commit()
            st.warning(f"Antrag {doc_key} wurde gelöscht.")
            st.rerun()

        show_verwaltung_application(doc_key)

def show_verwaltung_application(doc_key):
    meta = get_metadata(doc_key)
    if not meta:
        st.info("Es liegt noch kein Antrag vor.")
        return

    schritt = meta["prozesschritt"]
    zustand = meta["zustand"]
    bemerkung = meta["bemerkung"]

    st.write(f"**Aktueller Prozessschritt:** {schritt} | **Zustand:** {zustand}")
    doc = tiny_db.search(Query().doc_key == doc_key)
    if doc:
        doc_item = doc[0]
        antrag_data = doc_item.get("antrag_data", {})
        verwendungsnachweise = doc_item.get("verwendungsnachweise", [])
    else:
        doc_item = None
        antrag_data = {}
        verwendungsnachweise = []

    st.subheader("Antragsdaten:")
    st.json(antrag_data)

    if schritt is None:
        st.info("Der Antrag wurde vom Bürger noch nicht eingereicht.")
        return

    if schritt == "I":
        st.info("Antrag liegt zur Entscheidung vor (Übergang zu Schritt II).")
        if st.button("Antragsentscheidung beginnen (Schritt II)"):
            d, t = current_datetime()
            update_metadata(doc_key, prozesschritt="II", datum_antragsentscheidung=d, uhrzeit_antragsentscheidung=t)
            st.rerun()

    elif schritt == "II":
        st.subheader("Antragsentscheidung")
        chosen = st.radio("Entscheidung", ["OK", "Nicht OK"], index=0)
        begruendung = st.text_area("Bemerkung / Begründung (optional)")

        if st.button("Entscheidung speichern"):
            if chosen == "OK":
                update_metadata(doc_key, zustand="OK", bemerkung=begruendung)
                st.success("Antrag genehmigt (OK). Bürger kann jetzt Verwendungsnachweise erbringen.")
            else:
                update_metadata(doc_key, zustand="Nicht OK", bemerkung=begruendung)
                st.warning("Antrag wurde auf 'Nicht OK' gesetzt. Bürger sieht die Begründung.")
            st.rerun()

    elif schritt == "III":
        st.subheader("Verwendungsnachweise prüfen (Schritt III -> IV)")

        if not verwendungsnachweise:
            st.info("Bisher keine Verwendungsnachweise hinterlegt.")
            return

        st.write("Aktuell hinterlegte Verwendungsnachweise:")
        for idx, vn in enumerate(verwendungsnachweise):
            st.write(f"**{idx+1}**. {vn}")

        # Möglichkeit: Mehrere Verwendungsnachweise selektieren
        indices = list(range(len(verwendungsnachweise)))
        selected_indices = st.multiselect("Wähle Verwendungsnachweise zur Prüfung", indices)

        chosen = st.radio("Ergebnis für ausgewählte Nachweise", ["OK", "Nicht OK"], index=0)
        begruendung = st.text_area("Bemerkung / Begründung (optional)")

        if st.button("Ausgewählte Nachweise prüfen"):
            # Falls "Nicht OK": Der Bürger muss nachbessern
            if chosen == "Nicht OK":
                update_metadata(doc_key, zustand="Nicht OK", bemerkung=begruendung)
                st.warning("Verwendungsnachweise sind 'Nicht OK'. Bürger muss nachbessern.")
            else:
                st.success("Die ausgewählten Nachweise wurden als OK markiert.")
                # Du könntest hier z. B. in doc_item einzelne Nachweise als "geprüft" kennzeichnen
                # oder ein separates Feld "status" in jedem Nachweis ablegen.
                # Für Einfachheit belassen wir es bei einem globalen Zustand.

        if st.button("Alle Nachweise endgültig prüfen und Antrag abschließen"):
            d, t = current_datetime()
            update_metadata(doc_key, prozesschritt="IV", zustand="OK",
                            datum_antragsabschluss=d, uhrzeit_antragsabschluss=t, bemerkung=begruendung)
            st.success("Alle Nachweise OK. Antrag abgeschlossen (IV).")
            st.rerun()

    elif schritt == "IV":
        st.success("Der Antrag befindet sich im Abschluss-Schritt (IV).")
        st.write(f"Aktueller Zustand: {zustand}")
        st.write(f"Bemerkung: {bemerkung if bemerkung else '-'}")

        # Verwaltung kann Entscheidung korrigieren
        if zustand == "OK":
            if st.button("Entscheidung korrigieren (zurück auf 'Nicht OK')"):
                update_metadata(doc_key, zustand="Nicht OK")
                st.rerun()
        else:
            if st.button("Entscheidung korrigieren (doch 'OK')"):
                update_metadata(doc_key, zustand="OK")
                st.rerun()