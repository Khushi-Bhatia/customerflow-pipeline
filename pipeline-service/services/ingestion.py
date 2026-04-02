# import requests

# def fetch_all_customers():
#     all_data = []
#     page = 1
#     limit = 5

#     while True:
#         url = f"http://mock-server:5000/api/customers?page={page}&limit={limit}"
#         response = requests.get(url)
#         data = response.json()["data"]

#         if not data:
#             break

#         all_data.extend(data)
#         page += 1

#     return all_data
import requests
from sqlalchemy.orm import Session
from models.customer import Customer
from database import SessionLocal

FLASK_URL = "http://mock-server:5000/api/customers"


def ingest_data():
    db: Session = SessionLocal()
    page = 1
    limit = 10
    total_processed = 0

    while True:
        response = requests.get(f"{FLASK_URL}?page={page}&limit={limit}")
        data = response.json()

        customers = data.get("data", [])

        if not customers:
            break

        for c in customers:
            existing = db.query(Customer).filter(Customer.customer_id == c["customer_id"]).first()

            if existing:
                # update
                for key, value in c.items():
                    setattr(existing, key, value)
            else:
                # insert
                new_customer = Customer(**c)
                db.add(new_customer)

            total_processed += 1

        db.commit()
        page += 1

    db.close()

    return {"status": "success", "records_processed": total_processed}