from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load data from JSON
with open('data/customers.json') as f:
    customers = json.load(f)

# GET all customers (with pagination)
@app.route('/api/customers')
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "data": customers[start:end],
        "total": len(customers),
        "page": page,
        "limit": limit
    })

# GET single customer
@app.route('/api/customers/<customer_id>')
def get_customer(customer_id):
    for c in customers:
        if c["customer_id"] == customer_id:
            return jsonify(c)

    return jsonify({"error": "Customer not found"}), 404

# Health check
@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/')
def home():
    return "Flask server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)