# 🍽️ Restaurant Reservation System

Sistema di gestione prenotazioni per ristorante sviluppato con Django. Permette agli utenti di effettuare prenotazioni online e allo staff di gestirle attraverso un'interfaccia web moderna e intuitiva.

## ✨ Caratteristiche

- **Autenticazione utenti**: Sistema completo di registrazione e login
- **Gestione prenotazioni**: Creazione, visualizzazione ed eliminazione prenotazioni
- **Validazione intelligente**: Controlli automatici su date, orari e capacità
- **Pannello staff**: Funzionalità avanzate per confermare ed eliminare prenotazioni
- **Design responsive**: Interfaccia ottimizzata per desktop e dispositivi mobili

## 🛠️ Tecnologie Utilizzate

- **Backend**: Django 5.2.7
- **Frontend**: HTML, CSS
- **Autenticazione**: Django Auth System

## 📋 Requisiti

- Python 3.8+
- Django 5.2.7
- pip (gestore pacchetti Python)

## 🚀 Installazione

1. **Clona il repository**
```bash
git clone https://github.com/Thomas05017/ResBooking.git
cd restaurant
```

2. **Crea un ambiente virtuale**
```bash
python -m venv .venv
source .venv/bin/activate  # Su Windows: .venv\Scripts\activate
```

3. **Installa le dipendenze**
```bash
pip install django
```

4. **Esegui le migrazioni**
```bash
python manage.py migrate
```

5. **Crea un superutente (opzionale)**
```bash
python manage.py createsuperuser
```

6. **Avvia il server di sviluppo**
```bash
python manage.py runserver
```

7. **Accedi all'applicazione**
Apri il browser e vai su: `http://127.0.0.1:8000/`

## 📁 Struttura del Progetto

```
restaurant/
├── manage.py
├── restaurant/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── reservations/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── static/
    │   └── css/
    │       └── style.css
    └── templates/
        ├── registration/
        │   ├── login.html
        │   └── register.html
        └── reservations/
            ├── home.html
            └── create_reservation.html
```

## 🎯 Funzionalità Principali

### Per gli Utenti

- **Registrazione**: Creazione account con username, email e password
- **Login/Logout**: Accesso sicuro al sistema
- **Nuova Prenotazione**: Form guidato con validazione in tempo reale
- **Visualizza Prenotazioni**: Lista personale delle prenotazioni effettuate
- **Stati Prenotazioni**: Visualizzazione stato (In attesa/Confermata)

### Per lo Staff

- **Dashboard Completa**: Visualizzazione di tutte le prenotazioni
- **Conferma Prenotazioni**: Approvazione delle richieste di prenotazione
- **Eliminazione**: Possibilità di rimuovere qualsiasi prenotazione
- **Gestione Utenti**: Accesso al pannello admin di Django

## ⚙️ Configurazione

Le seguenti regole sono configurate nel sistema:

- **Orario di apertura**: 18:00 - 22:00
- **Ospiti per prenotazione**: Min 1, Max 20
- **Prenotazioni**: Non consentite per date passate
- **Vincolo unicità**: Un utente non può prenotare due volte lo stesso orario nella stessa data

## 🎨 Personalizzazione Design

I colori e lo stile sono configurabili tramite variabili CSS in `reservations/static/css/style.css`:

```css
:root {
    --primary-color: #2c5f7d;
    --secondary-color: #e8936f;
    --success-color: #28a745;
    /* ... altre variabili ... */
}
```

## 🔐 Sicurezza

- CSRF Protection attivo su tutti i form
- Password hashate con algoritmi sicuri di Django
- Login richiesto per tutte le operazioni di prenotazione

## 📱 Responsive Design

L'applicazione è completamente responsive con breakpoint a:
- Desktop: > 768px
- Tablet: 768px
- Mobile: < 480px

## 🐛 Debug

Per attivare la modalità debug, in `restaurant/settings.py`:

```python
DEBUG = True  # Solo per sviluppo!
```
---

**Buon appetito! 🍝**
