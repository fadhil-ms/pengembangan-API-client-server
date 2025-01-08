from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

# Konfigurasi database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "db_laptop"
}

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Endpoint untuk membuat laptop baru
@app.route('/laptops', methods=['POST'])
def create_laptop():
    data = request.get_json()
    brand = data.get('brand')
    model = data.get('model')
    price = data.get('price')
    specs = data.get('specs')

    if not (brand and model and price and specs):
        return jsonify({"error": "Semua data laptop harus diisi"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO laptops (brand, model, price, specs) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (brand, model, price, specs))
        connection.commit()
        laptop_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return jsonify({"id": laptop_id, "brand": brand, "model": model, "price": price, "specs": specs}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk mendapatkan semua laptop
@app.route('/laptops', methods=['GET'])
def read_all_laptops():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM laptops"
        cursor.execute(query)
        laptops = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(laptops), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk mendapatkan laptop berdasarkan ID
@app.route('/laptops/<int:laptop_id>', methods=['GET'])
def read_laptop_by_id(laptop_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM laptops WHERE id = %s"
        cursor.execute(query, (laptop_id,))
        laptop = cursor.fetchone()
        cursor.close()
        connection.close()

        if not laptop:
            return jsonify({"error": "Laptop tidak ditemukan"}), 404

        return jsonify(laptop), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk memperbarui laptop
@app.route('/laptops/<int:laptop_id>', methods=['PUT'])
def update_laptop(laptop_id):
    data = request.get_json()
    brand = data.get('brand')
    model = data.get('model')
    price = data.get('price')
    specs = data.get('specs')

    if not (brand and model and price and specs):
        return jsonify({"error": "Semua data laptop harus diisi"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Cek apakah laptop ada
        query = "SELECT * FROM laptops WHERE id = %s"
        cursor.execute(query, (laptop_id,))
        laptop = cursor.fetchone()
        if not laptop:
            return jsonify({"error": "Laptop tidak ditemukan"}), 404

        # Update data
        query = "UPDATE laptops SET brand = %s, model = %s, price = %s, specs = %s WHERE id = %s"
        cursor.execute(query, (brand, model, price, specs, laptop_id))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"id": laptop_id, "brand": brand, "model": model, "price": price, "specs": specs}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk menghapus laptop
@app.route('/laptops/<int:laptop_id>', methods=['DELETE'])
def delete_laptop(laptop_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = "DELETE FROM laptops WHERE id = %s"
        cursor.execute(query, (laptop_id,))
        connection.commit()
        row_count = cursor.rowcount
        cursor.close()
        connection.close()

        if row_count == 0:
            return jsonify({"error": "Laptop tidak ditemukan"}), 404

        return jsonify({"message": f"Laptop dengan ID {laptop_id} berhasil dihapus"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
