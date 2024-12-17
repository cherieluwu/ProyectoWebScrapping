from scrapers import ScraperJumbo, ScraperUnimarc, ScraperSantaIsabel
from pymongo import MongoClient
from datetime import datetime
import time

def test_scraping():
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['precio_comparador']
    
    # Inicializar scrapers
    scrapers = {
        'jumbo': ScraperJumbo(),
        'unimarc': ScraperUnimarc(),
        'santaisabel': ScraperSantaIsabel()
    }
    
    # Obtener un producto de prueba
    url_doc = db.urls.find_one()
    if not url_doc:
        print("No hay URLs en la base de datos")
        return
    
    print(f"Probando scraping para producto ID: {url_doc['product_id']}")
    
    # Probar cada scraper
    for tienda, scraper in scrapers.items():
        try:
            print(f"\nProbando {tienda}...")
            print(f"URL: {url_doc[tienda]}")
            
            inicio = time.time()
            precio = scraper.obtener_precio(url_doc[tienda])
            tiempo = time.time() - inicio
            
            print(f"Precio obtenido: {precio}")
            print(f"Tiempo de respuesta: {tiempo:.2f} segundos")
            
            # Limpiar y convertir precio
            if isinstance(precio, str):
                precio_limpio = ''.join(filter(str.isdigit, precio))
                precio_numero = int(precio_limpio) if precio_limpio else 0
                print(f"Precio limpio: {precio_numero}")
            
        except Exception as e:
            print(f"Error en {tienda}: {str(e)}")
        
        # Esperar 2 segundos entre requests
        time.sleep(2)

if __name__ == "__main__":
    test_scraping() 