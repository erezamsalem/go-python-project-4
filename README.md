Product Management System (Python-Flask & Swagger)
This is a full-stack web application featuring a Python Flask backend and a Vanilla JavaScript frontend. It allows users to manage a product catalog with full CRUD (Create, Read, Update, Delete) functionality, backed by a PostgreSQL database.

🚀 Features
RESTful API: Robust backend built with Flask.

Interactive Documentation: Integrated Swagger UI (via Flasgger) for real-time API testing.

Frontend: A clean, responsive UI for managing products.

Database: Persistent storage using PostgreSQL.

Dockerized: Includes Dockerfile and docker-compose.yml for easy deployment.

🛠️ Project Structure
Plaintext

.
├── static/              # Frontend files (HTML, CSS, JS)
├── venv/                # Python virtual environment
├── app.py               # Main Flask application with Swagger docs
├── .env                 # Environment variables (DB credentials)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration for the app
└── docker-compose.yml   # Multi-container orchestration
⚙️ Installation & Setup
1. Local Setup
Clone the directory and navigate to the project folder.

Create and activate a virtual environment:

PowerShell

python -m venv venv
.\venv\Scripts\Activate.ps1
Install dependencies:

PowerShell

pip install -r requirements.txt
Configure .env: Ensure your DATABASE_URL is set correctly:

Plaintext

DATABASE_URL=postgresql://user:password@localhost:5432/dbname
Run the application:

PowerShell

python app.py
2. Docker Setup (Recommended)
If you have Docker installed, simply run:

PowerShell

docker-compose up --build
📖 API Documentation (Swagger)
Once the application is running, you can access the interactive Swagger UI to test the endpoints:

🔗 URL: http://localhost:5000/apidocs/

Available Endpoints:
GET /products: Retrieve all products.

POST /products: Add a new product.

GET /products/{id}: Get details of a specific product.

PUT /products/{id}: Update an existing product.

DELETE /products/{id}: Remove a product.

🌐 Frontend Access
To use the web management interface, navigate to: 🔗 http://127.0.0.1:5000

🌐 swagger
🔗 http://127.0.0.1:5000/apidocs/

🧪 Dependencies
Flask: Web framework.

Psycopg: PostgreSQL adapter.

Flasgger: Swagger UI integration.

Flask-CORS: Handling Cross-Origin Resource Sharing.

Python-Dotenv: Environment variable management.