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