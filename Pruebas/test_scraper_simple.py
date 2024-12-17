from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class SimpleScraperJumbo:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()

    def buscar_productos(self, query):
        url = f"https://www.jumbo.cl/busqueda?ft={query}"
        print(f"Buscando en: {url}")
        
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            print(f"Status Code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Imprimir parte del HTML para debug
            print("Contenido de la página:")
            print(soup.prettify()[:500])  # Primeros 500 caracteres
            
            productos = []
            # Selector específico para productos en Jumbo
            items = soup.select('.product-item')
            print(f"Encontrados {len(items)} productos")
            
            for item in items[:5]:
                try:
                    nombre = item.select_one('.product-title')
                    precio = item.select_one('.product-price')
                    url = item.select_one('a')
                    imagen = item.select_one('img')
                    
                    if nombre and precio:
                        producto = {
                            'nombre': nombre.text.strip(),
                            'precio': ''.join(filter(str.isdigit, precio.text)),
                            'url': 'https://www.jumbo.cl' + url['href'] if url else '',
                            'imagen': imagen['src'] if imagen else '',
                            'tienda': 'jumbo',
                            'ultima_actualizacion': datetime.now()
                        }
                        productos.append(producto)
                        print(f"Producto encontrado: {producto['nombre']} - ${producto['precio']}")
                except Exception as e:
                    print(f"Error procesando producto: {str(e)}")
            
            return productos
            
        except Exception as e:
            print(f"Error en la búsqueda: {str(e)}")
            print(f"Respuesta completa: {response.text if 'response' in locals() else 'No response'}")
            return []

def test_scraper():
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['precio_comparador']
    
    # Crear instancia del scraper
    scraper = SimpleScraperJumbo()
    
    # Lista de productos para buscar
    productos_buscar = ['aceite', 'arroz', 'leche']
    
    for query in productos_buscar:
        print(f"\nBuscando {query}...")
        productos = scraper.buscar_productos(query)
        
        # Guardar en MongoDB
        for producto in productos:
            db.productos.update_one(
                {
                    'nombre': producto['nombre'],
                    'tienda': producto['tienda']
                },
                {'$set': producto},
                upsert=True
            )
        
        # Esperar 3 segundos entre búsquedas
        time.sleep(3)
    
    # Verificar resultados
    total_productos = db.productos.count_documents({})
    print(f"\nTotal de productos guardados: {total_productos}")
    
    print("\nAlgunos productos guardados:")
    for producto in db.productos.find().limit(3):
        print(f"- {producto['nombre']} (${producto['precio']}) en {producto['tienda']}")

if __name__ == "__main__":
    test_scraper()
    