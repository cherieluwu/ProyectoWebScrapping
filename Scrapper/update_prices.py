from pymongo import MongoClient
from scrapers import (
    ScraperJumbo, ScraperUnimarc, ScraperLider, 
    ScraperTottus, ScraperAcuenta
)
from datetime import datetime
import time
import schedule
import logging
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scraper.log'
)

def connect_db():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        return client['precio_comparador']
    except Exception as e:
        logging.error(f"Error conectando a MongoDB: {str(e)}")
        raise

def update_prices():
    db = connect_db()
    scrapers = {
        'jumbo': ScraperJumbo(),
        'unimarc': ScraperUnimarc(),
        'lider': ScraperLider(),
        'tottus': ScraperTottus(),
        'acuenta': ScraperAcuenta()
    }
    
    try:
        # Obtener todas las URLs de productos
        urls_collection = db.urls.find()
        
        for url_doc in urls_collection:
            product_id = url_doc['product_id']
            precios = {}
            
            # Obtener precios de cada tienda
            for tienda, scraper in scrapers.items():
                if tienda in url_doc and url_doc[tienda]:
                    try:
                        precio = scraper.obtener_precio(url_doc[tienda])
                        if isinstance(precio, str):
                            precio_limpio = ''.join(filter(str.isdigit, precio))
                            precios[tienda] = int(precio_limpio) if precio_limpio else 0
                        else:
                            precios[tienda] = 0
                        
                        logging.info(f"Precio obtenido para {tienda}: {precios[tienda]}")
                        time.sleep(random.uniform(1, 3))  # Delay aleatorio entre requests
                        
                    except Exception as e:
                        logging.error(f"Error obteniendo precio de {tienda} para producto {product_id}: {str(e)}")
                        precios[tienda] = 0
            
            if any(precios.values()):  # Si al menos un precio fue obtenido
                # Guardar precios en historial
                historial = {
                    'product_id': product_id,
                    'fecha': datetime.now(),
                    'precios': precios
                }
                db.historial_precios.insert_one(historial)
                
                # Actualizar precio actual
                db.productos.update_one(
                    {'id': product_id},
                    {'$set': {
                        'precios_actuales': precios,
                        'ultima_actualizacion': datetime.now()
                    }}
                )
                
                logging.info(f"Precios actualizados para producto {product_id}")
            
    except Exception as e:
        logging.error(f"Error general en update_prices: {str(e)}")
    finally:
        # Cerrar todos los scrapers
        for scraper in scrapers.values():
            try:
                scraper.__del__()
            except:
                pass

def run_scheduler():
    logging.info("Iniciando scheduler de actualización de precios")
    
    # Actualizar precios inmediatamente al iniciar
    update_prices()
    
    # Programar actualizaciones cada 8 horas
    schedule.every(8).hours.do(update_prices)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler() 