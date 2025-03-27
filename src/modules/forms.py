import streamlit as st
import datetime
import json

def load_config(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def convert_dates(obj):
    """
    Rekursive Funktion, um alle date-Objekte in ISO-String umzuwandeln,
    damit TinyDB sie speichern kann.
    """
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(v) for v in obj]
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    else:
        return obj

def render_fields(fields_config, prefix=""):
    """
    Rekursive Funktion zum Darstellen der Felder.
    Gibt ein Dictionary mit den eingegebenen Werten zurück.
    """
    result = {}
    for key, val in fields_config.items():
        # Verschachtelte Strukturen
        if isinstance(val, dict) and "type" not in val:
            # Keine 'type' => Unterstruktur
            st.subheader(key)
            result[key] = render_fields(val, prefix=prefix + key + "_")
        else:
            field_type = val.get("type")
            label = val.get("label", key)
            default = val.get("default") if val.get("default") else ""
            full_key = prefix + key

            if field_type == "text":
                result[key] = st.text_input(label, value=default, key=full_key)
            elif field_type == "date":
                try:
                    default_date = datetime.datetime.strptime(default, "%Y-%m-%d").date()
                except:
                    default_date = datetime.date.today()
                result[key] = st.date_input(label, value=default_date, key=full_key)
            elif field_type == "phone":
                result[key] = st.text_input(label, value=default, key=full_key)
            elif field_type == "email":
                result[key] = st.text_input(label, value=default, key=full_key)
            elif field_type == "checkbox":
                default_bool = bool(default)
                result[key] = st.checkbox(label, value=default_bool, key=full_key)
            elif field_type == "checkbox_group":
                options = val.get("options", [])
                if not isinstance(default, list):
                    default = []
                result[key] = st.multiselect(label, options, default=default, key=full_key)
            elif field_type == "radio":
                options = val.get("options", [])
                if default in options:
                    default_idx = options.index(default)
                else:
                    default_idx = 0
                result[key] = st.radio(label, options, index=default_idx, key=full_key)
            elif field_type == "number":
                try:
                    default_num = float(default)
                except:
                    default_num = 0
                result[key] = st.number_input(label, value=default_num, key=full_key)
            else:
                st.write(f"Unbekannter Feldtyp: {field_type}")
    return result