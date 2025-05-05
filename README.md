# 🏁 MOTORSPORT ARENA

Motorsport Arena è una piattaforma web pensata per gli appassionati di motorsport e gaming, dove gli utenti possono registrarsi, creare community, gestire eventi e interagire tra loro in modo sicuro e strutturato.

---

## 📌 Funzionalità principali

- Registrazione e login con JWT via cookie
- Blacklist dei token in logout
- Creazione e gestione di community
- Sistema di ruoli per le community
- Validazioni avanzate dei dati utente
- API sicure e protette da autenticazione JWT (via cookie)

---

## 🔌 API disponibili

| Endpoint                            | Metodo | Descrizione                                               |
|-------------------------------------|--------|------------------------------------------------------------|
| `/auth/register/`                   | POST   | Registrazione nuovo utente                                |
| `/auth/login/`                      | POST   | Login utente (JWT via cookie)                             |
| `/auth/logout/`                     | POST   | Logout utente e blacklist del refresh token               |
| `/network/community/create/`        | POST   | Crea una nuova community                                  |
| `/network/community/delete/<name>/` | DELETE | Elimina una community (solo admin della stessa)           |
| `/network/community/join/<name>/`   | POST   | Unisciti a una community tramite nome                     |
| `/network/community/leave/<name>/`  | POST   | Lascia una community                                      |

> ✨ Maggiori endpoint saranno aggiunti con lo sviluppo.

---

## ⚙️ Setup del progetto

### 1. 🔐 Crea il file `.env`

Nella root del progetto, crea un file chiamato `.env` con le seguenti variabili (in base a `settings.py`):
### Test
- DEBUG=True
### DataBase
- DB_NAME=MOTORSPORTARENA
- DB_USER=postgres
- DB_PASSWORD=your_database_password
- DB_HOST=localhost
- DB_PORT=5432
- SECRET_KEY=your_secret_key

## 🔌 Comandi Base Terminale Windows 

| Comando                           | Descrizione                                                                     |
|-----------------------------------|---------------------------------------------------------------------------------|
| `python -m venv .venv`            | Crea un ambiente virtuale Python nella cartella .venv                           |
| `.venv\Scripts\activate`          | (Windows) Attiva l’ambiente virtuale su Windows                                 |
| `pip install -r requirements.txt` | Installa tutte le dipendenze elencate nel file requirements.txt                 |
| `python manage.py makemigrations` | Prepara le migrazioni per eventuali modifiche ai modelli                        |
| `python manage.py migrate`        | Applica le migrazioni al database, creando le tabelle                           |
| `python manage.py runserver`      | Avvia il server di sviluppo Django su http://127.0.0.1:8000                     |
| `python manage.py createsuperuser`| (Facoltativo) Crea un utente admin per accedere all’interfaccia di admin Django |

