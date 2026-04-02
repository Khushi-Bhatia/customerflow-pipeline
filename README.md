# 🚀 CustomerFlow Pipeline

A Dockerized data pipeline application that simulates customer data ingestion using Flask, FastAPI, and PostgreSQL.

---

## 📌 Project Overview

This project demonstrates a simple **ETL (Extract, Transform, Load) pipeline**:

**Flow:**
Flask (Mock API) → FastAPI (Ingestion Service) → PostgreSQL (Database) → API Response

---

## 🧱 Tech Stack

* **Python 3.10+**
* **Flask** – Mock data provider
* **FastAPI** – Data ingestion & API service
* **PostgreSQL** – Database
* **SQLAlchemy** – ORM
* **Docker & Docker Compose** – Containerization

---

## 📂 Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

Make sure you have installed:

* Docker Desktop (running)
* Python 3.10+
* Git

Check versions:

```
docker --version
docker-compose --version
```

---

### 2️⃣ Run the Application

From project root:

```
docker-compose up --build
```

This will start:

* Flask server → http://localhost:5000
* FastAPI server → http://localhost:8000
* PostgreSQL database → port 5432

---

## 🔗 API Endpoints

### 🔹 Flask Mock Server (Port 5000)

| Endpoint              | Method | Description             |
| --------------------- | ------ | ----------------------- |
| `/api/customers`      | GET    | Get paginated customers |
| `/api/customers/{id}` | GET    | Get single customer     |
| `/api/health`         | GET    | Health check            |

Example:

```
http://localhost:5000/api/customers?page=1&limit=5
```

---

### 🔹 FastAPI Service (Port 8000)

#### 1. Ingest Data

```
POST /api/ingest
```

✔ Fetches all data from Flask
✔ Inserts/updates into PostgreSQL

Response:

```
{
  "status": "success",
  "records_processed": 20
}
```

---

#### 2. Get Customers

```
GET /api/customers?page=1&limit=10
```

---

#### 3. Get Single Customer

```
GET /api/customers/{customer_id}
```

---

#### Swagger UI:

```
http://localhost:8000/docs
```

---

## 🔄 Data Flow

1. Flask serves customer data from JSON file
2. FastAPI fetches paginated data
3. Data is inserted/updated in PostgreSQL
4. FastAPI exposes APIs to query stored data

---

## 📌 Notes

* Ensure `customers.json` contains **20+ records**
* Run ingestion before fetching data from FastAPI
* Docker must be running before executing commands

