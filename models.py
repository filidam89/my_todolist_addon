from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.String(250))
    frequenza = db.Column(db.String(50))  # es. "giornaliero", "settimanale", ecc.
    prossima_esecuzione = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    punteggio = db.Column(db.Integer, default=0)
    assegnato_a = db.Column(db.String(10), default="")  # "A", "B", "AB"
    stato = db.Column(db.String(20), default="pendente")  # "pendente", "completato"
    # Campo per salvare le persone confermate per il completamento
    confermato_da = db.Column(db.String(10), default="")  # "A", "B", "AB", o vuoto

    def aggiorna_prossima_esecuzione(self):
        # Esempio: se la frequenza è "giornaliero"
        if self.frequenza == "giornaliero":
            self.prossima_esecuzione += timedelta(days=1)
        elif self.frequenza == "settimanale":
            self.prossima_esecuzione += timedelta(weeks=1)
        # Aggiungere altre logiche in base alle necessità
