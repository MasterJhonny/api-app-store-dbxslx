from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Habilitar CORS para toda la aplicación
CORS(app)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",  # Obtener de google cloud
    scope,
)

client = gspread.authorize(creds)

# ruta general
@app.route('/', methods=["GET"])
def home():
    return jsonify({"message":"HOME GET!!!"}), 201
# Ruta para manejar los productos
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        try:
            sheet = client.open("db-tienda").sheet1
            # Abrir el documento
            list_details = sheet.col_values(2)
            list_prices = sheet.col_values(3)
            list_image_urls = sheet.col_values(4)

            # Crear una lista de diccionarios
            list_products = [
                {
                    "detail": detail,
                    "price": price,
                    "image_url": image_url
                }
                for detail, price, image_url in zip(list_details, list_prices, list_image_urls)
            ]

            # retornar el resultado
            return jsonify(list_products)
        except gspread.exceptions.SpreadsheetNotFound:
            return jsonify({"error": "Product not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Ocurrió un error: {e}"}), 404        
    elif request.method == 'POST':
        return jsonify({"message":"Product created!"}), 201

# Ruta para actualizar un producto
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    print("valor de: ", id)
    if id:
        print("asd")
    else:
        return jsonify({"error": "Product not found"}), 404

# Ruta para eliminar un producto
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    # pass
    if id:
        return jsonify({"message": f"Product deleted id: {id}"})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)