from flask import jsonify

def admin_dashboard():
    facturas = [
        {"id": 1, "usuario": "admin", "total": 100.0, "fecha": "2024-12-01"},
        {"id": 2, "usuario": "admin", "total": 200.0, "fecha": "2024-12-02"}
    ]
    return jsonify(facturas)

def student_dashboard():
    facturas = [
        {"id": 3, "usuario": "estudiante", "total": 50.0, "fecha": "2024-12-03"}
    ]
    return jsonify(facturas)
