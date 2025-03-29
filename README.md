# Zuwendungsapp

Die **Zuwendungsapp** ist ein Proof-of-Concept für ein modular aufgebautes, demoartiges Webanwendungssystem für ein mehrstufiges Antragsverfahren. Zuwendungsverfahren nach den §/Art. 44 B/LHO standen Pate. In der Anwendung können Bürger mehrere Anträge erstellen, bearbeiten und löschen – während Verwaltungsmitarbeiter die Anträge prüfen, Entscheidungen treffen, Verwendungsnachweise verwalten und bei Bedarf auch einzelne Einträge löschen können. Die Anwendung basiert auf Streamlit, TinyDB und SQLite.

**Wichtig**: Es handelt sich lediglich um ein Grundgerüst zu Demonstrations- und Testzwecken. Anpassungen im Bereich Datenhaltung, Nutzerverwaltung etc. wären vor einem Versuch, das System zu produktiv zu setzen empfohlen. Wer möchte, darf die App gerne für seine Zwecke weiterverwerten.

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

- **Datenbankzugriffe:**  
  - SQLite-Zugriffe erfolgen synchron mit `sqlite`. Sie dienen für die Anreicherung der Nutzdaten um Metadaten.  
  - Synchrone TinyDB-Operationen werden für die Nutzdaten verwendet.

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

````
Zuwendungsapp/
├─ data/
│  ├─ data.json         # TinyDB-Datenbank
│  └─ metadata.db       # SQLite-Datenbank
├─ docs/                # Dokumentation
│  ├─ video.mov         # Demovideo
├─ tests/               # Modultests und Integrationstests
│  ├─ test_modultests.py
│  └─ test_integration.py
├─ src/
│  ├─ __init__.py
│  ├─ main.py           # Einstiegspunkt der Streamlit-App
│  ├─ config/
│  │  ├─ antrag_config.json
│  │  └─ nachweis_config.json
│  ├─ db/
│  │  ├─ __init__.py
│  │  └─ connection.py  # SQLite-Verbindung und TinyDB-Zugriff
│  └─ modules/
│     ├─ __init__.py
│     ├─ user_management.py
│     ├─ metadata_management.py
│     ├─ forms.py
│     ├─ antrag_logic.py
│     └─ verwaltung_logic.py
├─ Dockerfile           # Docker-Build-Konfiguration
└─ requirements.txt     # Abhängigkeiten
````

## Installation und Setup

1. **Clone das Repository:**

   ```bash
   git clone https://github.com/<repositoryurl>.git
   cd zuwendungsapp
   ```

2. **Python-Abhängigkeiten installieren:**

    Erstelle ein virtuelles Environment und installiere die benötigten Pakete:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. **Datenbank initialisieren:**

    Stelle sicher, dass sich im Ordner data/ die Dateien data.json und metadata.db befinden. Falls nicht, werden diese bei der ersten Ausführung der Anwendung automatisch erzeugt.

## Ausführen der Anwendung

Navigiere in das Hauptverzeichnis und starte die Anwendung mit Streamlit:

```bash
cd zuwendungsapp
streamlit run src/main.py
```

## Docker

Um die Anwendung in einem Docker-Container auszuführen:

2. **Docker-Image bauen:**

    ```bash
    docker build -t zuwendungsapp .
    ```

2.	**Container starten:**

    ```bash
    docker run -p 8501:8501 zuwendungsapp
    ```

    Die Anwendung ist dann unter http://localhost:8501 erreichbar.

## Tests

Die Tests befinden sich im Verzeichnis `tests/`. Um die Tests auszuführen, navigiere in den tests/-Ordner und führe die folgenden Befehle aus:

```bash
cd tests
python -m unittest test_modultests.py
python -m unittest test_integration.py
```

## Dokumentation

Die Dokumentation befindet sich im Verzeichnis `docs/`. Dort findet sich ein kleines Demovideo, das die "Idee" illustrieren soll, ein antragsbasiertes Verwaltungsverfahren als Kollaboration zwischen Verwaltung und Antragstellenden aufzufassen.

## Contributing

Beiträge sind willkommen! Verwerte den Code gerne weiter für deine eigenen Anwendungen zur Digitalisierung von Verfahren.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
