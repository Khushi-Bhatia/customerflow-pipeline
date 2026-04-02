# from fastapi import FastAPI, HTTPException
# from database import SessionLocal, engine
# from models.customer import Customer, Base
# from services.ingestion import fetch_all_customers

# app = FastAPI()


# import time
# from sqlalchemy import text
# from sqlalchemy.exc import OperationalError

# # Wait for DB to be ready
# while True:
#     try:
#         with engine.connect() as connection:
#             connection.execute(text("SELECT 1"))
#         print("Database is ready!")
#         break
#     except OperationalError:
#         print("Database not ready... retrying in 2 seconds")
#         time.sleep(2)

# # Now create tables
# Base.metadata.create_all(bind=engine)

# # Base.metadata.create_all(bind=engine)

# @app.post("/api/ingest")
# def ingest_data():
#     db = SessionLocal()
#     customers = fetch_all_customers()

#     for c in customers:
#         existing = db.query(Customer).filter_by(customer_id=c["customer_id"]).first()

#         if existing:
#             for key, value in c.items():
#                 setattr(existing, key, value)
#         else:
#             db.add(Customer(**c))

#     db.commit()

#     return {"status": "success", "records_processed": len(customers)}

# @app.get("/api/customers")
# def get_customers(page: int = 1, limit: int = 10):
#     db = SessionLocal()
#     query = db.query(Customer)

#     total = query.count()
#     data = query.offset((page - 1) * limit).limit(limit).all()

#     return {
#         "data": [c.__dict__ for c in data],
#         "total": total,
#         "page": page,
#         "limit": limit
#     }

# @app.get("/api/customers/{customer_id}")
# def get_customer(customer_id: str):
#     db = SessionLocal()
#     customer = db.query(Customer).filter_by(customer_id=customer_id).first()

#     if not customer:
#         raise HTTPException(status_code=404, detail="Customer not found")

#     return customer.__dict__



from fastapi import FastAPI, HTTPException
from database import SessionLocal, engine
from models.customer import Customer, Base
from services.ingestion import ingest_data

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import time

app = FastAPI()


# ✅ Wait for DB to be ready
while True:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database is ready!")
        break
    except OperationalError:
        print("Database not ready... retrying in 2 seconds")
        time.sleep(2)


# ✅ Create tables
Base.metadata.create_all(bind=engine)


# ✅ Ingest API (clean)
@app.post("/api/ingest")
def ingest():
    return ingest_data()


# ✅ Get all customers (paginated)
@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db = SessionLocal()

    query = db.query(Customer)
    total = query.count()

    customers = query.offset((page - 1) * limit).limit(limit).all()

    result = []
    for c in customers:
        result.append({
            "customer_id": c.customer_id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address,
            "date_of_birth": c.date_of_birth,
            "account_balance": float(c.account_balance),
            "created_at": c.created_at
        })

    return {
        "data": result,
        "total": total,
        "page": page,
        "limit": limit
    }


# ✅ Get single customer
@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()

    customer = db.query(Customer).filter_by(customer_id=customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "customer_id": customer.customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "date_of_birth": customer.date_of_birth,
        "account_balance": float(customer.account_balance),
        "created_at": customer.created_at
    }