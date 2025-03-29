# Beispielhaftes Dockerfile
FROM python:3.12-slim

WORKDIR /app

# requirements.txt ins Image kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY src/ ./src/
COPY data/ ./data/
COPY docs/ ./docs/

EXPOSE 8501

CMD ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]