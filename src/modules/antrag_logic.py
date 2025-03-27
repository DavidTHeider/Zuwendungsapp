import streamlit as st
import datetime
import uuid

from tinydb import Query
from db.connection import tiny_db
from modules.metadata_management import get_metadata, update_metadata
from modules.forms import load_config, render_fields, convert_dates
from modules.user_management import logout
from db.connection import conn, cursor

def current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

def buerger_view():
    st.header("Bürger-Sicht")

    # 1) Button "Neuen Antrag anlegen"
    if st.button("Neuen Antrag anlegen"):
        doc_key = str(uuid.uuid4())
        tiny_db.insert({
            "doc_key": doc_key,
            "antrag_data": {},
            "owner": st.session_state["username"],
            "verwendungsnachweise": []  # Liste für mehrere Nachweise
        })
        update_metadata(doc_key, owner=st.session_state["username"])
        st.success(f"Neuer Antrag wurde angelegt (ID: {doc_key}).")
        st.rerun()

    # 2) Liste aller Anträge des aktuellen Bürgers
    cursor.execute("SELECT doc_key FROM metadata WHERE owner=?", (st.session_state["username"],))
    rows = cursor.fetchall()
    doc_keys = [r[0] for r in rows]

    if not doc_keys:
        st.info("Sie haben noch keine Anträge gestellt.")
        return

    # Auswahlbox
    selected_doc_key = st.selectbox("Wähle einen Antrag zur Bearbeitung", doc_keys)

    # Button zum Löschen dieses Antrags
    if st.button("Diesen Antrag löschen"):
        # Aus TinyDB entfernen
        tiny_db.remove(Query().doc_key == selected_doc_key)
        # Metadaten löschen
        cursor.execute("DELETE FROM metadata WHERE doc_key=?", (selected_doc_key,))
        conn.commit()
        st.warning(f"Antrag {selected_doc_key} wurde gelöscht.")
        st.rerun()

    # Anzeige des gewählten Antrags
    show_buerger_application(selected_doc_key)

def show_buerger_application(doc_key):
    meta = get_metadata(doc_key)
    doc = tiny_db.search(Query().doc_key == doc_key)
    doc_item = doc[0] if doc else None

    schritt = meta["prozesschritt"] if meta else None
    zustand = meta["zustand"] if meta else None
    bemerkung = meta["bemerkung"] if meta else None

    # Schritt I, Korrektur etc. -> Antragsformular
    if schritt in [None, "I"] or (schritt == "II" and zustand == "Nicht OK"):
        st.subheader("Antragsformular (Schritt I)")

        antrag_cfg = load_config("src/config/antrag_config.json")
        config_fields = antrag_cfg["antrag"]["fields"]

        existing_data = {}
        if doc_item and "antrag_data" in doc_item:
            existing_data = doc_item["antrag_data"]

        with st.form("antrag_form"):
            # Werte als Default eintragen
            for top_key, top_val in config_fields.items():
                if isinstance(top_val, dict):
                    for field_key, field_def in top_val.items():
                        if top_key in existing_data and field_key in existing_data[top_key]:
                            field_def["default"] = existing_data[top_key][field_key]

            rendered_data = render_fields(config_fields)
            if st.form_submit_button("Antrag absenden"):
                rendered_data = convert_dates(rendered_data)

                # Speichern
                if doc_item:
                    doc_item["antrag_data"] = rendered_data
                    tiny_db.update(doc_item, Query().doc_key == doc_key)
                else:
                    # Neuer Datensatz
                    new_doc = {
                        "doc_key": doc_key,
                        "antrag_data": rendered_data,
                        "owner": st.session_state["username"],
                        "verwendungsnachweise": []
                    }
                    tiny_db.insert(new_doc)

                d, t = current_datetime()
                if schritt is None:
                    update_metadata(doc_key, prozesschritt="I", zustand="OK",
                                    datum_antragstellung=d, uhrzeit_antragstellung=t, bemerkung=None)
                elif schritt == "I":
                    update_metadata(doc_key, prozesschritt="I", zustand="OK",
                                    datum_antragstellung=d, uhrzeit_antragstellung=t, bemerkung=None)
                elif schritt == "II" and zustand == "Nicht OK":
                    update_metadata(doc_key, zustand="OK", datum_antragstellung=d,
                                    uhrzeit_antragstellung=t, bemerkung=None)
                st.success("Antragsdaten wurden gespeichert.")

    elif schritt == "II":
        # Wartet auf Entscheidung oder genehmigt
        if zustand == "Nicht OK":
            st.warning("Die Verwaltung hat Ihren Antrag abgelehnt.")
            st.info("Bitte korrigieren Sie Ihren Antrag im Formular (s. oben).")
        else:
            st.info("Die Verwaltung hat Ihren Antrag genehmigt (Schritt II abgeschlossen).")
            st.info("Sie können jetzt Verwendungsnachweise einreichen.")
            if st.button("Zum Nachweisformular wechseln"):
                d, t = current_datetime()
                update_metadata(doc_key, prozesschritt="III", zustand="OK",
                                datum_antragsnachweis=d, uhrzeit_antragsnachweis=t)
                st.rerun()

    elif schritt == "III":
        st.subheader("Verwendungsnachweise (Schritt III)")

        if doc_item:
            verwendungsnachweise = doc_item.get("verwendungsnachweise", [])
        else:
            verwendungsnachweise = []

        if zustand == "Nicht OK" and bemerkung:
            st.warning(f"Bemerkung der Verwaltung: {bemerkung}")

        # Liste aller Verwendungsnachweise anzeigen + Löschfunktion
        if verwendungsnachweise:
            st.write("Bisher erfasste Verwendungsnachweise:")
            for idx, vn in enumerate(verwendungsnachweise):
                st.write(f"**{idx+1}**. {vn}")
                if st.button(f"Löschen Verwendungsnachweis #{idx+1}", key=f"del_vn_{idx}"):
                    verwendungsnachweise.pop(idx)
                    doc_item["verwendungsnachweise"] = verwendungsnachweise
                    tiny_db.update(doc_item, Query().doc_key == doc_key)
                    st.rerun()

        # Button "Neuen Verwendungsnachweis hinzufügen"
        if st.button("Verwendungsnachweis hinzufügen"):
            verwendungsnachweise.append({"beschreibung": "", "betrag": 0})
            doc_item["verwendungsnachweise"] = verwendungsnachweise
            tiny_db.update(doc_item, Query().doc_key == doc_key)
            st.rerun()

        # Formular zur Bearbeitung aller Verwendungsnachweise
        if verwendungsnachweise:
            with st.form("verwendungsnachweis_form"):
                nachweis_cfg = load_config("src/config/nachweis_config.json")
                # Wir gehen jedes Objekt durch und rendern es
                updated_nachweise = []
                for idx, vn in enumerate(verwendungsnachweise):
                    st.write(f"**Verwendungsnachweis #{idx+1}**")
                    # Default-Werte eintragen
                    flds = nachweis_cfg["nachweis"]["fields"]["liste_verwendungsnachweise"]
                    for field_key, field_def in flds.items():
                        if field_key in vn:
                            field_def["default"] = vn[field_key]
                    # Rendern
                    res = render_fields(flds, prefix=f"vn_{idx}_")
                    updated_nachweise.append(res)

                if st.form_submit_button("Speichern"):
                    # updated_nachweise ist eine Liste von Dicts
                    # wir konvertieren Datumsobjekte, falls vorhanden
                    updated_nachweise = convert_dates(updated_nachweise)
                    # Speichern
                    doc_item["verwendungsnachweise"] = updated_nachweise
                    tiny_db.update(doc_item, Query().doc_key == doc_key)
                    st.success("Verwendungsnachweise aktualisiert. Die Verwaltung wird prüfen.")

    elif schritt == "IV":
        if zustand == "OK":
            st.success("Ihr Antrag wurde final genehmigt. Verfahren beendet.")
        else:
            st.warning("Die Verwaltung hat Ihre Verwendungsnachweise als 'Nicht OK' eingestuft.")
            st.info("Bitte bessern Sie Ihre Nachweise nach (Schritt III).")
            if st.button("Erneut zu den Verwendungsnachweisen"):
                update_metadata(doc_key, prozesschritt="III", bemerkung=None)
                st.rerun()