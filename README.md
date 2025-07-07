# 📦 Catalogue Management System

A full-stack web application for managing catalogues with user authentication, CRUD operations, date validation, and RESTful APIs documented using Swagger UI.

## 🚀 Features

- 🔐 User login with validation  
- 📋 Add, update, delete, and view catalogues  
- 📆 Start and end date validations  
- ✅ Active/Inactive catalogue status  
- 🌐 RESTful API with Swagger documentation  
- 🧪 Unit testing with Pytest  
- 📄 Logging for all key operations  

## 🛠️ Tech Stack

| Layer     | Technology                     |
|-----------|--------------------------------|
| Frontend  | HTML, CSS, JavaScript (Fetch API) |
| Backend   | Python, Flask, Flask-CORS       |
| Database  | MySQL                           |
| Docs      | Swagger UI (via Flasgger)       |
| Testing   | Pytest                          |
| Logging   | Python logging                  |

## 📁 Project Structure

```
catalogue-management-system/
├── app.py                     # Main Flask app
├── service/                   # Business logic (catalogue & auth services)
├── dto/                       # Data Transfer Object for catalogue
├── util/                      # Utility modules (e.g., logger)
├── templates/                 # HTML templates (login.html, index.html)
├── static/                    # CSS/JavaScript files
├── tests/                     # Pytest test cases
├── app.log                    # Log file
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/catalogue-management-system.git
cd catalogue-management-system
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Sample `requirements.txt`:

```
flask
flask-cors
flasgger
pytest
mysql-connector-python
```

### 4. Configure MySQL

Ensure you have MySQL running and update the database connection inside the `catalogue_service.py` file with your credentials.

## ▶️ Running the App

```bash
python app.py
```

- App URL: http://localhost:5050  
- Swagger Docs: http://localhost:5050/apidocs

## 📘 API Endpoints (via Swagger)

| Method | Endpoint            | Description               |
|--------|---------------------|---------------------------|
| POST   | /login              | Login with credentials    |
| GET    | /catalogues         | Get all catalogues        |
| POST   | /catalogues         | Create a new catalogue    |
| GET    | /catalogues/<id>    | Get a catalogue by ID     |
| PUT    | /catalogues/<id>    | Update a catalogue        |
| DELETE | /catalogues/<id>    | Delete a catalogue        |

## 🧪 Running Tests

```bash
pytest
```

Runs all test cases located in the `/tests` directory.

## 📄 Logging

All operations such as creation, updates, deletions, and errors are logged in `app.log`.

## 📜 License

This project was created as part of an internship assignment.  
Feel free to use, share, and build upon it.

## 🙋‍♂️ Author

**Karthik R**  
Intern Project – 2025  
[GitHub Profile](https://github.com/your-username)
