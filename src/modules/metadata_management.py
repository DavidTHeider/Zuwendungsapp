import sqlite3
from ..db.connection import conn, cursor

def get_metadata(doc_key):
    cursor.execute("SELECT * FROM metadata WHERE doc_key=?", (doc_key,))
    row = cursor.fetchone()
    if row:
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    return None

def update_metadata(doc_key, **kwargs):
    meta = get_metadata(doc_key)
    if not meta:
        # Anlegen
        fields = ["doc_key", "owner", "prozesschritt", "zustand",
                  "datum_antragstellung", "uhrzeit_antragstellung",
                  "datum_antragsentscheidung", "uhrzeit_antragsentscheidung",
                  "datum_antragsnachweis", "uhrzeit_antragsnachweis",
                  "datum_antragsabschluss", "uhrzeit_antragsabschluss",
                  "bemerkung"]
        data = {f: None for f in fields}
        data["doc_key"] = doc_key
        data.update(kwargs)
        placeholders = ",".join(["?"]*len(fields))
        cursor.execute(f"INSERT INTO metadata ({','.join(fields)}) VALUES ({placeholders})",
                       tuple(data[f] for f in fields))
    else:
        # Update
        set_clause = []
        vals = []
        for k, v in kwargs.items():
            set_clause.append(f"{k}=?")
            vals.append(v)
        set_clause_str = ", ".join(set_clause)
        vals.append(doc_key)
        cursor.execute(f"UPDATE metadata SET {set_clause_str} WHERE doc_key=?", tuple(vals))
    conn.commit()