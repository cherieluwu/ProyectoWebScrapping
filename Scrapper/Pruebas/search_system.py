from pymongo import MongoClient
from datetime import datetime
import concurrent.futures
import time
from scrapers import (
    ScraperLider, ScraperAcuenta, ScraperTrebol, 
    ScraperJumbo, ScraperUnimarc, ScraperSantaIsabel,
    ScraperMercadoLibre
)

class SearchSystem:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['precio_comparador']
        self.scrapers = {
            'lider': ScraperLider(),
            'acuenta': ScraperAcuenta(),
            'trebol': ScraperTrebol(),
            'jumbo': ScraperJumbo(),
            'unimarc': ScraperUnimarc(),
            'santaisabel': ScraperSantaIsabel(),
            'mercadolibre': ScraperMercadoLibre()
        }
    
    def actualizar_catalogo(self):
        """Actualiza el catálogo completo de productos"""
        # Lista de términos de búsqueda comunes
        terminos_busqueda = [
            "aceite", "arroz", "azúcar", "leche", "pan", 
            "huevos", "pasta", "detergente", "papel higiénico",
            # ... más términos ...
        ]
        
        for termino in terminos_busqueda:
            self.buscar_y_guardar(termino)
            time.sleep(2)  # Evitar sobrecarga
    
    def buscar_y_guardar(self, query):
        """Busca productos en todas las tiendas y guarda resultados"""
        print(f"Buscando: {query}")
        
        # Usar ThreadPoolExecutor para búsquedas paralelas
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(scraper.buscar_productos, query): tienda
                for tienda, scraper in self.scrapers.items()
            }
            
            for future in concurrent.futures.as_completed(futures):
                tienda = futures[future]
                try:
                    productos = future.result()
                    self._guardar_productos(productos, tienda)
                except Exception as e:
                    print(f"Error en {tienda}: {str(e)}")
    
    def _guardar_productos(self, productos, tienda):
        """Guarda o actualiza productos en la base de datos"""
        for producto in productos:
            # Normalizar nombre para mejor búsqueda
            nombre_norm = self._normalizar_nombre(producto['nombre'])
            
            # Actualizar o insertar producto
            self.db.productos.update_one(
                {
                    'nombre_normalizado': nombre_norm,
                    'tienda': tienda
                },
                {
                    '$set': {
                        'nombre': producto['nombre'],
                        'precio': producto['precio'],
                        'url': producto['url'],
                        'imagen': producto['imagen'],
                        'ultima_actualizacion': datetime.now()
                    }
                },
                upsert=True
            )
    
    def _normalizar_nombre(self, nombre):
        """Normaliza el nombre del producto para mejor búsqueda"""
        return nombre.lower().strip() 