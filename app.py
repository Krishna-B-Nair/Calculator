"""
Flask Calculator API
---------------------
A small backend project demonstrating:
- Routes (@app.route)
- HTTP methods (GET, POST)
- Request/response handling (request.get_json(), jsonify())
- JSON input/output
- Basic Python (functions, error handling)

Run with:
    pip install flask
    python app.py

Then test with curl or Postman, e.g.:
    curl -X POST http://127.0.0.1:5000/add -H "Content-Type: application/json" -d "{\"a\": 5, \"b\": 3}"
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for calculation history (resets when server restarts)
history = []


def get_numbers(data):
    """
    Extract and validate 'a' and 'b' from the request JSON.
    Returns (a, b, error_message). error_message is None if valid.
    """
    if data is None:
        return None, None, "Request body must be JSON"

    if "a" not in data or "b" not in data:
        return None, None, "Both 'a' and 'b' are required"

    try:
        a = float(data["a"])
        b = float(data["b"])
    except (ValueError, TypeError):
        return None, None, "'a' and 'b' must be numbers"

    return a, b, None


def record(operation, a, b, result):
    """Save a calculation to history."""
    history.append({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    })


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json(silent=True)
    a, b, error = get_numbers(data)
    if error:
        return jsonify({"error": error}), 400

    result = a + b
    record("add", a, b, result)
    return jsonify({"result": result}), 200


@app.route("/subtract", methods=["POST"])
def subtract():
    data = request.get_json(silent=True)
    a, b, error = get_numbers(data)
    if error:
        return jsonify({"error": error}), 400

    result = a - b
    record("subtract", a, b, result)
    return jsonify({"result": result}), 200


@app.route("/multiply", methods=["POST"])
def multiply():
    data = request.get_json(silent=True)
    a, b, error = get_numbers(data)
    if error:
        return jsonify({"error": error}), 400

    result = a * b
    record("multiply", a, b, result)
    return jsonify({"result": result}), 200


@app.route("/divide", methods=["POST"])
def divide():
    data = request.get_json(silent=True)
    a, b, error = get_numbers(data)
    if error:
        return jsonify({"error": error}), 400

    if b == 0:
        return jsonify({"error": "Cannot divide by zero"}), 400

    result = a / b
    record("divide", a, b, result)
    return jsonify({"result": result}), 200


@app.route("/history", methods=["GET"])
def get_history():
    return jsonify({"history": history}), 200


@app.route("/history", methods=["DELETE"])
def clear_history():
    history.clear()
    return jsonify({"message": "History cleared"}), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Calculator API is running",
        "routes": {
            "POST /add": "{'a': number, 'b': number} -> {'result': number}",
            "POST /subtract": "{'a': number, 'b': number} -> {'result': number}",
            "POST /multiply": "{'a': number, 'b': number} -> {'result': number}",
            "POST /divide": "{'a': number, 'b': number} -> {'result': number}",
            "GET /history": "returns list of past calculations",
            "DELETE /history": "clears history"
        }
    }), 200


if __name__ == "__main__":
    app.run(debug=True)