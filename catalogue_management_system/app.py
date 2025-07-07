from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from service.catalogue_service import CatalogueService
from service.auth_service import AuthService
from dto.catalogue_dto import Catalogue
from datetime import datetime
from flasgger import Swagger, swag_from
import sys
import traceback
import logging
import socket

app = Flask(__name__)
CORS(app)
Swagger(app)

service = CatalogueService()
auth_service = AuthService()

# -------------------------- Logging Configuration --------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

#-------------------------- Standard Response Functions --------------------------
def success_response(message, data=None, status_code=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status_code


def error_response(message, error_type="BadRequest", details="", status_code=400):
    return jsonify({
        "success": False,
        "message": message,
        "error": {
            "type": error_type,
            "details": details
        }
    }), status_code

# -------------------------- Date Parsing --------------------------
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        pass
    try:
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y-%m-%d")
    except:
        pass
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
    except:
        pass
    return date_str

# -------------------------- Routes --------------------------

@app.route('/')
def home():
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'username', 'in': 'formData', 'type': 'string', 'required': True
        },
        {
            'name': 'password', 'in': 'formData', 'type': 'string', 'required': True
        }
    ],
    'responses': {
        200: {'description': 'Login successful'},
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        is_form = False
    else:
        data = request.form
        username = data.get("username")
        password = data.get("password")
        is_form = True

    if not username or not password:
        if is_form:
            return render_template("login.html", error="Username and password are required.")
        return error_response("Username and password are required", "ValidationError")

    try:
        if auth_service.authenticate(username, password):
            logger.info(f"Login successful for user: {username}")
            if is_form:
                return redirect(url_for('index'))
            return success_response("Login successful", {"username": username})
        else:
            logger.warning(f"Login failed for user: {username}")
            if is_form:
                return render_template("login.html", error="Invalid username or password.")
            return error_response("Invalid username or password", "AuthenticationError", status_code=401)
    except Exception as e:
        logger.error(f"Login exception: {str(e)}")
        if is_form:
            return render_template("login.html", error="Login failed. Please try again.")
        return error_response("Login failed", "LoginError", str(e), 500)


@app.route('/index')
def index():
    try:
        catalogues = service.get_all_catalogues()
        logger.info(f"Fetched {len(catalogues)} catalogues from DB")
        return render_template("index.html", catalogues=catalogues)
    except Exception as e:
        logger.error(f"Error loading index: {str(e)}")
        return error_response("Failed to load index page", "HomePageError", str(e), 500)


@app.route('/catalogues', methods=['GET'])
@swag_from({
    'tags': ['Catalogue'],
    'responses': {
        200: {'description': 'List of all catalogues'}
    }
})
def get_all():
    try:
        catalogues = service.get_all_catalogues()
        logger.info(f"API fetch: {len(catalogues)} catalogues")
        return success_response("All catalogues fetched", [cat.__dict__ for cat in catalogues])
    except Exception as e:
        logger.error(f"Error fetching catalogues: {str(e)}")
        return error_response("Failed to fetch catalogues", "FetchError", str(e), 500)


@app.route('/catalogues', methods=['POST'])
@swag_from({
    'tags': ['Catalogue'],
    'parameters': [
        {'name': 'catalogue_id', 'in': 'json', 'type': 'integer', 'required': True},
        {'name': 'name', 'in': 'json', 'type': 'string', 'required': True},
        {'name': 'description', 'in': 'json', 'type': 'string', 'required': True},
        {'name': 'start_date', 'in': 'json', 'type': 'string', 'required': True},
        {'name': 'end_date', 'in': 'json', 'type': 'string', 'required': True},
        {'name': 'is_active', 'in': 'json', 'type': 'integer', 'required': True}
    ],
    'responses': {
        201: {'description': 'Catalogue created successfully'}
    }
})
def create():
    data = request.json
    if not data:
        return error_response("No JSON data received")

    if 'id' in data:
        data['catalogue_id'] = data['id']
    if 'status' in data:
        data['is_active'] = data['status']

    required_fields = ['catalogue_id', 'name', 'description', 'start_date', 'end_date', 'is_active']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error_response("Missing fields", "ValidationError", f"Missing: {missing}", 400)

    try:
        start_date = parse_date(data['start_date'])
        end_date = parse_date(data['end_date'])
        cat = Catalogue(
            int(data['catalogue_id']), data['name'], data['description'],
            start_date, end_date, int(data['is_active'])
        )
        service.create_catalogue(cat)
        logger.info(f"Catalogue created: ID={data['catalogue_id']}, Name={data['name']}")
        return success_response("Catalogue created", status_code=201)
    except Exception as e:
        logger.error(f"Error creating catalogue: {str(e)}")
        traceback.print_exc()
        return error_response("Error saving catalogue", "InsertError", str(e), 500)


@app.route('/catalogues/<int:cat_id>', methods=['PUT'])
def update(cat_id):
    data = request.json
    if not data:
        return error_response("No JSON data received")

    required = ['name', 'description', 'start_date', 'end_date', 'is_active']
    missing = [f for f in required if f not in data]
    if missing:
        return error_response("Missing fields", "ValidationError", f"Missing: {missing}", 400)

    try:
        start_date = parse_date(data['start_date'])
        end_date = parse_date(data['end_date'])
        cat = Catalogue(
            cat_id, data['name'], data['description'],
            start_date, end_date, int(data['is_active'])
        )
        service.update_catalogue_by_id(cat_id, cat)
        logger.info(f"Catalogue updated: ID={cat_id}")
        return success_response("Catalogue updated")
    except Exception as e:
        logger.error(f"Error updating catalogue {cat_id}: {str(e)}")
        traceback.print_exc()
        return error_response("Error updating catalogue", "UpdateError", str(e), 400)


@app.route('/catalogues/<int:cat_id>', methods=['DELETE'])
def delete(cat_id):
    try:
        service.delete_catalogue_by_id(cat_id)
        logger.info(f"Catalogue deleted: ID={cat_id}")
        return success_response("Catalogue deleted")
    except Exception as e:
        logger.error(f"Error deleting catalogue {cat_id}: {str(e)}")
        return error_response("Error deleting catalogue", "DeleteError", str(e), 404)


@app.route('/catalogues/<int:cat_id>', methods=['GET'])
def get_catalogue(cat_id):
    try:
        cat = service.get_catalogue_by_id(cat_id)
        logger.info(f"Fetched catalogue: ID={cat_id}")
        return success_response("Catalogue fetched", cat.__dict__)
    except Exception as e:
        logger.error(f"Catalogue not found: ID={cat_id}, Error={str(e)}")
        return error_response("Catalogue not found", "NotFoundError", str(e), 404)


@app.route('/logout', methods=['POST'])
def logout():
    logger.info("User logged out")
    return redirect(url_for('login_page'))


@app.errorhandler(403)
def forbidden(e):
    logger.warning(f"403 Forbidden: {str(e)}")
    return error_response("Access forbidden", "Forbidden", str(e), 403)


# -------------------------- Main --------------------------
if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"\n🟢 Flask app is accessible at: http://{local_ip}:5050")
    print(f"🔴 Swagger UI available at: http://{local_ip}:5050/apidocs\n")
    app.run(host="0.0.0.0", port=5050, debug=True)
