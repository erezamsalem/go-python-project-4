import os
import psycopg
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import time

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Database connection URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establishes a connection to the database with retries."""
    retries = 5
    delay = 2
    while retries > 0:
        try:
            conn = psycopg.connect(DATABASE_URL)
            return conn
        except psycopg.OperationalError as e:
            print(f"Could not connect to database: {e}. Retrying in {delay} seconds...")
            retries -= 1
            time.sleep(delay)
    print("Could not connect to the database after several retries. Exiting.")
    return None

def create_products_table():
    """Create the products table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        print("Skipping table creation due to failed database connection.")
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price NUMERIC(10, 2) NOT NULL
                );
            """)
            conn.commit()
            print("Table 'products' checked/created successfully.")
    except psycopg.Error as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()

# Ensure the table exists when the application starts
create_products_table()

# --- Serve Frontend ---
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# --- API Endpoints ---

# POST /products - Create a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Invalid request body"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id;"
            cur.execute(sql, (data['name'], data['price']))
            product_id = cur.fetchone()[0]
            conn.commit()
            new_product = {'id': product_id, 'name': data['name'], 'price': data['price']}
            return jsonify(new_product), 201
    except psycopg.Error as e:
        return jsonify({"error": f"Failed to create product: {e}"}), 500
    finally:
        if conn:
            conn.close()

# GET /products - Get all products
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price FROM products ORDER BY id;")
            rows = cur.fetchall()
            products = [{'id': row[0], 'name': row[1], 'price': float(row[2])} for row in rows]
            return jsonify(products), 200
    except psycopg.Error as e:
        return jsonify({"error": f"Failed to query products: {e}"}), 500
    finally:
        if conn:
            conn.close()

# GET /products/<id> - Get a single product
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price FROM products WHERE id = %s;", (id,))
            row = cur.fetchone()
            if row is None:
                return jsonify({"error": "Product not found"}), 404
            product = {'id': row[0], 'name': row[1], 'price': float(row[2])}
            return jsonify(product), 200
    except psycopg.Error as e:
        return jsonify({"error": f"Failed to query product: {e}"}), 500
    finally:
        if conn:
            conn.close()

# PUT /products/<id> - Update a product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Invalid request body"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            sql = "UPDATE products SET name = %s, price = %s WHERE id = %s;"
            cur.execute(sql, (data['name'], data['price'], id))
            if cur.rowcount == 0:
                return jsonify({"error": "Product not found"}), 404
            conn.commit()
            updated_product = {'id': id, 'name': data['name'], 'price': data['price']}
            return jsonify(updated_product), 200
    except psycopg.Error as e:
        return jsonify({"error": f"Failed to update product: {e}"}), 500
    finally:
        if conn:
            conn.close()

# DELETE /products/<id> - Delete a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM products WHERE id = %s;"
            cur.execute(sql, (id,))
            if cur.rowcount == 0:
                return jsonify({"error": "Product not found"}), 404
            conn.commit()
            return jsonify({"message": "Product deleted successfully"}), 200
    except psycopg.Error as e:
        return jsonify({"error": f"Failed to delete product: {e}"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # This block is still useful for running locally without Docker/Gunicorn
    port = int(os.environ.get("APP_PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
