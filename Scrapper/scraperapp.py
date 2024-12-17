from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['precio_comparador']

@app.route('/api/buscar')
def buscar_productos():
    query = request.args.get('q', '')
    categoria = request.args.get('categoria', '')
    min_precio = request.args.get('min_precio', type=int)
    max_precio = request.args.get('max_precio', type=int)
    
    # Construir el filtro de búsqueda
    filter_query = {
        '$or': [
            {'nombre': {'$regex': query, '$options': 'i'}},
            {'descripcion': {'$regex': query, '$options': 'i'}}
        ]
    }
    
    if categoria:
        filter_query['categoria'] = categoria
    
    # Obtener productos que coincidan con la búsqueda
    productos = list(db.productos.find(
        filter_query,
        {'_id': 0}
    ))
    
    # Filtrar por precio si se especificaron rangos
    if min_precio is not None or max_precio is not None:
        productos_filtrados = []
        for producto in productos:
            precios = producto.get('precios_actuales', {}).values()
            if not precios:
                continue
            
            precio_min = min(precio for precio in precios if precio > 0)
            if min_precio is not None and precio_min < min_precio:
                continue
            if max_precio is not None and precio_min > max_precio:
                continue
            
            productos_filtrados.append(producto)
        productos = productos_filtrados
    
    return jsonify({
        'success': True,
        'productos': productos
    })

@app.route('/api/categorias')
def obtener_categorias():
    categorias = db.productos.distinct('categoria')
    return jsonify({
        'success': True,
        'categorias': categorias
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)