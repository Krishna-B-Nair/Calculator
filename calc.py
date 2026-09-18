from flask import Flask, request, jsonify

app = Flask(__name__)
history =  []

def get_numbers(data):
    if data is None:
        return None, None, "Request body must be JSON"
    if "a" not in data or "b" not in data:
        return None, None, "Both 'a' and 'b' are required"
    try:
        a = float(data["a"])
        b = float(data["b"])
    except (ValueError,TypeError):
        return None, None, "'a' and 'b' must be in numbers"
    return a,b, None
def record(operation,a,b,result):
    """save calculations to history"""
    history.append({
        "operation":operation,
        "a":a,
        "b":b,
        "result":result
    })
@app.route("/add", method = ["POST"])
def add():
    data = request.get_json(silent = True)
    a, b, error = get_numbers(data)
    if error:
        return jsonify({"error":error}),400
    result = a + b
    record("add", a, b, result)
    return jsonify({"result":result}),200

