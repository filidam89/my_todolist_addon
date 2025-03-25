FROM python:3.9-slim

# Installazione delle dipendenze
RUN pip install flask flask_sqlalchemy

# Copia dei file dell'app
COPY app /app
WORKDIR /app

# Esposizione della porta (assicurarsi che la porta sia disponibile come configurata in Home Assistant)
EXPOSE 5000

CMD ["python", "main.py"]
