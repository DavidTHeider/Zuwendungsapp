import sqlite3
from tinydb import TinyDB

# TinyDB
tiny_db = TinyDB("data/data.json")

# SQLite
conn = sqlite3.connect("data/metadata.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    """
    Erstellt die notwendigen Tabellen in SQLite, falls sie nicht existieren.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            doc_key TEXT PRIMARY KEY,
            owner TEXT,
            prozesschritt TEXT,
            zustand TEXT,
            datum_antragstellung TEXT,
            uhrzeit_antragstellung TEXT,
            datum_antragsentscheidung TEXT,
            uhrzeit_antragsentscheidung TEXT,
            datum_antragsnachweis TEXT,
            uhrzeit_antragsnachweis TEXT,
            datum_antragsabschluss TEXT,
            uhrzeit_antragsabschluss TEXT,
            bemerkung TEXT
        )
    """)
    conn.commit()