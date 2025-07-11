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

