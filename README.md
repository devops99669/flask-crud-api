Here's a complete step-by-step guide to create a Flask CRUD API with:

✅ Flask REST API
✅ Dockerfile to containerize the app
✅ Swagger UI using flasgger (optional)
✅ Postman support
✅ Python-based file storage (no DB to keep it simple)

📁 Project Structure
Copy
Edit
flask-crud-api/
├── app.py
├── requirements.txt
└── Dockerfile
✅ app.py – Flask CRUD API
python
Copy
Edit
from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)  # Swagger UI at http://localhost:5000/apidocs

data_store = {}  # key-value store: id -> record

@app.route('/')
def index():
    return "Welcome to Flask CRUD API"

@app.route('/items', methods=['POST'])
def create_item():
    """
    Create a new item
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Item
          required:
            - id
            - name
          properties:
            id:
              type: string
            name:
              type: string
    responses:
      201:
        description: Item created
    """
    item = request.get_json()
    data_store[item['id']] = item
    return jsonify({"message": "Item created"}), 201

@app.route('/items', methods=['GET'])
def get_all_items():
    """Get all items
    ---
    responses:
      200:
        description: A list of items
    """
    return jsonify(list(data_store.values()))

@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by ID
    ---
    parameters:
      - in: path
        name: item_id
        required: true
        type: string
    responses:
      200:
        description: The item
      404:
        description: Item not found
    """
    item = data_store.get(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    """Update item by ID
    ---
    parameters:
      - in: path
        name: item_id
        required: true
        type: string
      - in: body
        name: body
        schema:
          properties:
            name:
              type: string
    responses:
      200:
        description: Updated item
    """
    if item_id not in data_store:
        return jsonify({"error": "Item not found"}), 404
    data_store[item_id].update(request.get_json())
    return jsonify(data_store[item_id])

@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item by ID
    ---
    parameters:
      - in: path
        name: item_id
        required: true
        type: string
    responses:
      200:
        description: Deletion status
    """
    if item_id in data_store:
        del data_store[item_id]
        return jsonify({"message": "Item deleted"})
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
✅ requirements.txt
txt
Copy
Edit
flask
flasgger
✅ Dockerfile
Dockerfile
Copy
Edit
# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
✅ Build & Run with Docker
bash
Copy
Edit
# Build the image
docker build -t flask-crud-api .

# Run the container
docker run -d -p 5000:5000 --name my_crud flask-crud-api
✅ Test with Postman or Swagger
🔗 Open browser: http://localhost:5000/apidocs → Swagger UI

Or use Postman with the following endpoints:

Method	Endpoint	Description
POST	/items	Create item
GET	/items	Get all items
GET	/items/<id>	Get item by ID
PUT	/items/<id>	Update item
DELETE	/items/<id>	Delete item

✅ Example POST Body (JSON)
json
Copy
Edit
{
  "id": "1",
  "name": "Laptop"
}
