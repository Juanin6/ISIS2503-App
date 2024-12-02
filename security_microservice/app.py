from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# Patrones para detectar posibles inyecciones SQL y XSS
SQL_PATTERN = re.compile(r"(?:')|(?:--)|(?:#)|(/\*(?:.|[\n\r])*?\*/)|(\b(SELECT|UPDATE|DELETE|INSERT|WHERE|DROP|ALTER|CREATE)\b)", re.IGNORECASE)
XSS_PATTERN = re.compile(r"<.*?>", re.IGNORECASE)

def is_malicious(data):
    if isinstance(data, str) and (SQL_PATTERN.search(data) or XSS_PATTERN.search(data)):
        return True
    if isinstance(data, dict):
        return any(is_malicious(value) for value in data.values())
    return False

@app.route('/validate', methods=['POST'])
def validate_request():
    data = request.json
    if is_malicious(data):
        return jsonify({"status": "blocked", "message": "Solicitud maliciosa detectada"}), 403
    
    # Reenviar la solicitud al backend principal si es válida
    response = requests.post("http://localhost:8000/users", json=data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5001)
