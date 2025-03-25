from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Task
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inizializzazione del DB se non esiste
with app.app_context():
    db.create_all()

def calcola_punteggi():
    """Calcola la differenza dei punteggi tra persona A e persona B."""
    tasks = Task.query.filter_by(stato="completato").all()
    punti_A = sum(task.punteggio for task in tasks if 'A' in task.confermato_da)
    punti_B = sum(task.punteggio for task in tasks if 'B' in task.confermato_da)
    return punti_A, punti_B, punti_A - punti_B

@app.route('/')
def index():
    # Recupera i task in attesa
    pending_tasks = Task.query.filter_by(stato="pendente").order_by(Task.prossima_esecuzione).all()
    punti_A, punti_B, differenza = calcola_punteggi()
    return render_template('index.html', tasks=pending_tasks, punti_A=punti_A, punti_B=punti_B, differenza=differenza)

@app.route('/aggiungi', methods=['POST'])
def aggiungi_task():
    titolo = request.form.get('titolo')
    descrizione = request.form.get('descrizione')
    frequenza = request.form.get('frequenza')
    punteggio = int(request.form.get('punteggio', 0))
    assegnato_a = request.form.get('assegnato_a')  # "A", "B" o "AB"
    
    nuovo_task = Task(
        titolo=titolo,
        descrizione=descrizione,
        frequenza=frequenza,
        punteggio=punteggio,
        assegnato_a=assegnato_a,
        prossima_esecuzione=datetime.utcnow()
    )
    db.session.add(nuovo_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/conferma/<int:task_id>', methods=['POST'])
def conferma_task(task_id):
    task = Task.query.get_or_404(task_id)
    # Il form permette di confermare la persona (oppure entrambe)
    confermato_da = request.form.get('confermato_da')
    task.confermato_da = confermato_da
    task.stato = "completato"
    # Aggiorna la prossima esecuzione in base alla frequenza
    task.aggiorna_prossima_esecuzione()
    # Se desideri mantenere lo storico, potresti creare un nuovo record per il task ripetuto
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/tasks')
def api_tasks():
    """Endpoint API per recuperare i task in attesa (utile per la webapp Android)."""
    tasks = Task.query.filter_by(stato="pendente").all()
    tasks_data = [
        {
            'id': task.id,
            'titolo': task.titolo,
            'descrizione': task.descrizione,
            'frequenza': task.frequenza,
            'prossima_esecuzione': task.prossima_esecuzione.isoformat(),
            'punteggio': task.punteggio,
            'assegnato_a': task.assegnato_a,
            'stato': task.stato,
            'confermato_da': task.confermato_da
        } for task in tasks
    ]
    return jsonify(tasks_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
