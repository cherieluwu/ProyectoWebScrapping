from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapers import ScraperJumbo, ScraperUnimarc, ScraperSantaIsabel
from urls import PRODUCT_URLS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)

@app.route('/api/productos')
def obtener_productos():
    productos = []
    for nombre, datos in PRODUCT_URLS.items():
        productos.append({
            'id': datos['id'],
            'nombre': nombre,
            'imagen': datos['imagen'],
            'descripcion': datos['descripcion']
        })
    return jsonify(productos)

@app.route('/api/precios')
def obtener_precios():
    product_id = request.args.get('id')
    include_urls = request.args.get('include_urls', 'false').lower() == 'true'
    
    # Encontrar el producto correspondiente
    producto = None
    urls = None
    for nombre, datos in PRODUCT_URLS.items():
        if datos['id'] == product_id:
            producto = nombre
            urls = {
                'jumbo': datos['jumbo'],
                'unimarc': datos['unimarc'],
                'santaisabel': datos['santaisabel']
            }
            break
    
    if not producto or not urls:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    try:
        scraper_jumbo = ScraperJumbo()
        scraper_unimarc = ScraperUnimarc()
        scraper_santaisabel = ScraperSantaIsabel()
        
        precios = {
            'jumbo': scraper_jumbo.obtener_precio(urls['jumbo']),
            'unimarc': scraper_unimarc.obtener_precio(urls['unimarc']),
            'santaisabel': scraper_santaisabel.obtener_precio(urls['santaisabel'])
        }
        
        # Limpiar y formatear precios
        for tienda, precio in precios.items():
            if isinstance(precio, str):
                precio_limpio = ''.join(filter(str.isdigit, precio))
                precios[tienda] = int(precio_limpio) if precio_limpio else 0
        
        # Devolver respuesta según el parámetro include_urls
        if include_urls:
            return jsonify({
                'precios': precios,
                'urls': urls
            })
        else:
            return jsonify(precios)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Intentar conectar con base de datos

app.config['MONGO_URI'] = 'mongodb://localhost:27017/BD1'  # Cambia esto según tu configuración
mongo = PyMongo(app)


if __name__ == "__main__":
    app.run(debug=True, port=5000)