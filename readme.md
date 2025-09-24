# Carbon Credit Ledger API

A simple backend API built with **FastAPI** and **SQLite** that tracks carbon credits lifecycle from creation to retirement of carbon credits using an **event-based ledger system**.

---

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite (for local development)
- Uvicorn (ASGI server)

---

## Features

- Add new carbon credit records (with a deterministic ID)
- Log "created" and "retired" events
- Retrieve complete credit record along with its event history
- Uses SQLite for simplicity

---
## API Endpoints

- POST /records – Create a new carbon credit record

- POST /records/{id}/retire – Retire an existing credit (adds a “retired” event)

- GET /records/{id} – Retrieve a record along with all events
## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/mohdgeelani/Carbon-Ledger-API.git
cd carbon_ledger_api
```
2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv env
env\Scripts\activate    
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
uvicorn main:app --reload
```

## Reflection Questions

***1. How did you design the ID so it’s always the same for the same input?***

I created the unique ID using SHA-256 hashing by combining important fields like project name, registry, vintage year, quantity, and serial number. This way, if the same data is given again, it will always generate the same ID. This helps avoid duplicates and keeps records consistent.

***2. Why did you use an event log instead of updating the record directly?***

I used events to keep a complete history of each record. Instead of changing the original data, every important action like creation or retirement is stored as a new event. This makes sure nothing is lost or changed by mistake, and we always know what happened and when. This  will helps analyzing carbon credit when it was created and when it was retired, gives full life time overview of carbon credits.

***3. If two people tried to retire the same credit at the same time, what would break? How would you fix it?***

If two people try to retire the same credit at the same time, it could create duplicate retire events. To fix this, I would add a rule to allow only one retired event per record or use a transaction to ensure duplicates cannot happen.
