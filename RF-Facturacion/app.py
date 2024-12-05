from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/admin/dashboard/')
def admin_dashboard():
    facturas = [
        {"id": 1, "usuario": "admin", "total": 100.0, "fecha": "2024-12-01"},
        {"id": 2, "usuario": "admin", "total": 200.0, "fecha": "2024-12-02"}
    ]
    return jsonify(facturas)

@app.route('/student/dashboard/')
def student_dashboard():
    facturas = [
        {"id": 3, "usuario": "estudiante", "total": 50.0, "fecha": "2024-12-03"}
    ]
    return jsonify(facturas)

if __name__ == '__main__':
    app.run(debug=True)
