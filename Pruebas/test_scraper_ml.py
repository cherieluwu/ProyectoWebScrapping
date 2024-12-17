import requests
from pymongo import MongoClient
from datetime import datetime
import time

class ScraperMercadoLibre:
    def __init__(self):
        self.base_url = "https://api.mercadolibre.com/sites/MLC/search"
        
    def buscar_productos(self, query):
        print(f"\nBuscando: {query}")
        
        params = {
            'q': query,
            'category': 'MLC1403', # Categoría Alimentos y Bebidas
            'limit': 10  # Limitamos a 10 productos por búsqueda
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            productos = []
            for item in data.get('results', []):
                try:
                    producto = {
                        'nombre': item['title'],
                        'precio': str(item['price']),
                        'url': item['permalink'],
                        'imagen': item['thumbnail'],
                        'tienda': 'mercadolibre',
                        'id_producto': item['id'],
                        'vendedor': item['seller']['nickname'],
                        'ultima_actualizacion': datetime.now()
                    }
                    productos.append(producto)
                    print(f"Producto encontrado: {producto['nombre']} - ${producto['precio']}")
                except Exception as e:
                    print(f"Error procesando producto: {str(e)}")
            
            return productos
            
        except Exception as e:
            print(f"Error en la búsqueda: {str(e)}")
            return []

def test_scraper():
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['precio_comparador']
    
    # Crear instancia del scraper
    scraper = ScraperMercadoLibre()
    
    # Lista de productos para buscar
    productos_buscar = [
        'aceite cocina',
        'arroz grado 1',
        'leche entera',
        'azúcar blanca',
        'pasta fideos'
    ]
    
    total_guardados = 0
    
    for query in productos_buscar:
        productos = scraper.buscar_productos(query)
        
        # Guardar en MongoDB
        for producto in productos:
            result = db.productos.update_one(
                {
                    'id_producto': producto['id_producto'],
                    'tienda': producto['tienda']
                },
                {'$set': producto},
                upsert=True
            )
            if result.modified_count > 0 or result.upserted_id:
                total_guardados += 1
        
        # Esperar 1 segundo entre búsquedas
        time.sleep(1)
    
    # Verificar resultados
    print(f"\nTotal de productos guardados: {total_guardados}")
    
    print("\nAlgunos productos guardados:")
    for producto in db.productos.find().limit(5):
        print(f"- {producto['nombre']}")
        print(f"  Precio: ${producto['precio']}")
        print(f"  Vendedor: {producto['vendedor']}")
        print(f"  URL: {producto['url']}")
        print("---")

if __name__ == "__main__":
    test_scraper()