# Zuwendungsapp

Die **Zuwendungsapp** ist ein modular aufgebautes, asynchron arbeitendes Webanwendungssystem für ein mehrstufiges Antragsverfahren. In der Anwendung können Bürger mehrere Anträge erstellen, bearbeiten und löschen – während Verwaltungsmitarbeiter die Anträge prüfen, Entscheidungen treffen, Verwendungsnachweise verwalten und bei Bedarf auch einzelne Einträge löschen können. Die Anwendung basiert auf Streamlit, TinyDB und aiosqlite, um gleichzeitige Zugriffe asynchron zu ermöglichen.

## Features

- **Mehrstufiges Antragsverfahren:**  
  - **Schritt I:** Antragstellung und ggf. Korrektur durch den Bürger  
  - **Schritt II:** Antragsentscheidung durch die Verwaltung  
  - **Schritt III:** Erfassung von Verwendungsnachweisen (mit der Möglichkeit, mehrere Nachweise hinzuzufügen)  
  - **Schritt IV:** Abschluss des Antragsverfahrens

- **Benutzerverwaltung:**  
  - Zwei Standardrollen: *Bürger* und *Verwaltung*  
  - Login/Logout-Funktionalität  
  - Jeder Benutzer kann nur seine eigenen Anträge sehen und bearbeiten

- **Asynchrone Datenbankzugriffe:**  
  - SQLite-Zugriffe erfolgen asynchron mit `aiosqlite`  
  - Synchrone TinyDB-Operationen werden in separate Threads ausgelagert (mittels `asyncio.to_thread`)

- **Modulare Architektur:**  
  - Der Code ist in mehrere Module und Pakete unterteilt:
    - **`db/`**: Datenbankverbindungen und Initialisierung
    - **`modules/`**:  
      - `user_management`: Login, Logout, Standardbenutzer
      - `metadata_management`: Verwaltung der Metadaten (SQLite)
      - `forms`: Dynamische Formularerzeugung und Hilfsfunktionen
      - `antrag_logic`: Logik der Bürger-Sicht (Anträge erstellen, bearbeiten, Verwendungsnachweise verwalten)
      - `verwaltung_logic`: Logik der Verwaltungs-Sicht (Anträge prüfen, Entscheidungen treffen)
    - **`config/`**: JSON-Konfigurationen für Antragsformulare und Nachweisformulare
  - Tests und Dokumentation sind in eigenen Verzeichnissen enthalten

- **Docker-Unterstützung:**  
  - Ein Dockerfile ermöglicht das einfache Verpacken und Deployen der Anwendung in Containern

## Projektstruktur

Zuwendungsapp/
├─ data/
│  ├─ data.json         # TinyDB-Datenbank
│  └─ metadata.db       # SQLite-Datenbank
├─ docs/                # Dokumentation (Sphinx, Markdown etc.)
├─ tests/               # Modultests und Integrationstests
│  ├─ test_modultests.py
│  └─ test_integration.py
├─ src/
│  ├─ init.py
│  ├─ main.py           # Einstiegspunkt der Streamlit-App
│  ├─ config/
│  │  ├─ antrag_config.json
│  │  └─ nachweis_config.json
│  ├─ db/
│  │  ├─ init.py
│  │  └─ connection.py  # Asynchrone SQLite-Verbindung und TinyDB-Zugriff
│  └─ modules/
│     ├─ init.py
│     ├─ user_management.py
│     ├─ metadata_management.py
│     ├─ forms.py
│     ├─ antrag_logic.py
│     └─ verwaltung_logic.py
├─ Dockerfile           # Docker-Build-Konfiguration
└─ requirements.txt     # Abhängigkeiten

## Installation und Setup

1. **Clone das Repository:**

   ```bash
   git clone https://github.com/DeinBenutzername/zuwendungsapp.git
   cd zuwendungsapp

	2.	Python-Abhängigkeiten installieren:
Erstelle ein virtuelles Environment und installiere die benötigten Pakete:

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


	3.	Datenbank initialisieren:
Stelle sicher, dass sich im Ordner data/ die Dateien data.json und metadata.db befinden. Falls nicht, werden diese bei der ersten Ausführung der Anwendung automatisch erzeugt.

Ausführen der Anwendung

Navigiere in das Hauptverzeichnis und starte die Anwendung mit Streamlit:

cd zuwendungsapp
streamlit run src/main.py

Wichtig: Für die asynchrone Variante sollte der Start aus dem Hauptverzeichnis erfolgen, sodass alle Modulpfade korrekt aufgelöst werden.

Docker

Um die Anwendung in einem Docker-Container auszuführen:
	1.	Docker-Image bauen:

docker build -t zuwendungsapp .


	2.	Container starten:

docker run -p 8501:8501 zuwendungsapp



Die Anwendung ist dann unter http://localhost:8501 erreichbar.

Tests

Die Tests befinden sich im Verzeichnis tests/. Um die Tests auszuführen, navigiere in den tests/-Ordner und führe die folgenden Befehle aus:

cd tests
python -m unittest test_modultests.py
python -m unittest test_integration.py

Dokumentation

Die Dokumentation befindet sich im Verzeichnis docs/. Du kannst dort beispielsweise Sphinx oder ein anderes Dokumentationssystem nutzen, um die Projektstruktur und API zu beschreiben.

Contributing

Beiträge sind willkommen! Bitte erstelle zuerst ein Issue, bevor du Pull Requests einreichst.

Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details findest du in der Datei LICENSE.

⸻

Für Fragen und weitere Informationen, wende dich bitte an deine.email@example.com.

