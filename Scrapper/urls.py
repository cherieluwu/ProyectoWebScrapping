from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys
import time
import json
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
from selenium.common.exceptions import TimeoutException

class JumboScraper:
    def __init__(self):
        print("[INFO] Iniciando Jumbo Scraper...")
        self.setup_driver()
        self.setup_database()
        self.base_url = "https://www.jumbo.cl"
        self.products_saved = 0
        self.products_updated = 0
        
        # Categorías normales
        self.categories = {
            'Frutas y Verduras': [
                '/frutas-y-verduras/frutas',
                '/frutas-y-verduras/verduras'
            ],
            'Carnicería': [
                '/carniceria/vacuno',
                '/carniceria/cerdo'
            ],
            'Despensa': [
                '/despensa/arroz-y-legumbres',
                '/despensa/pastas-y-salsas'
            ]
        }
        
        # URLs para aceites usando navegación por menú
        self.special_categories = {
            'Aceites y Vinagres': {
                'menu_path': [
                    ('Despensa', '/despensa'),
                    ('Aceites y Vinagres', None)
                ],
                'selectors': {
                    'menu_button': '.vtex-menu-2-x-menuItem',
                    'submenu': '.vtex-menu-2-x-submenu',
                    'category_link': 'a[href*="aceites"]',
                    'products': '.product-card'
                }
            }
        }
        
        # Configuración para API
        self.api_config = {
            'base_url': 'https://www.jumbo.cl/api/catalog_system/pub/products/search',
            'headers': {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'params': {
                '_from': '0',
                '_to': '49',
                'ft': 'aceites-y-vinagres',
                'sc': '73'  # ID de la categoría aceites
            }
        }

    def setup_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def setup_database(self):
        try:
            # Conectar a MongoDB con timeout explícito
            self.client = MongoClient('mongodb://localhost:27017/', 
                                    serverSelectionTimeoutMS=5000)
            
            # Verificar conexión
            self.client.admin.command('ping')
            
            self.db = self.client['taller']
            self.productos = self.db['productos']
            
            # Crear índices
            self.productos.create_index([
                ("nombre", ASCENDING),
                ("categoria", ASCENDING),
                ("subcategoria", ASCENDING)
            ], unique=True)
            
            # Verificar que podemos escribir
            test_doc = {
                "test": True,
                "timestamp": datetime.now()
            }
            test_result = self.productos.insert_one(test_doc)
            self.productos.delete_one({"_id": test_result.inserted_id})
            
            print("[INFO] MongoDB: Conexión y permisos verificados")
            
        except ServerSelectionTimeoutError:
            print("[ERROR] No se puede conectar a MongoDB. ¿Está corriendo el servidor?")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Error configurando MongoDB: {e}")
            sys.exit(1)

    def extract_product_info(self, product, category, subcategory):
        """Extraer información del producto con mejor manejo de estados"""
        try:
            # Intentar obtener el título con el nuevo selector
            nombre = product.find_element(
                By.CSS_SELECTOR, 
                '.vtex-product-summary-2-x-productBrand'
            ).text.strip()
            
            # Obtener el precio (con mejor manejo de errores)
            try:
                precio = product.find_element(By.CSS_SELECTOR, '.product-price').text.strip()
                precio = precio.replace('$', '').replace('.', '').strip()
                precio = int(precio) if precio.isdigit() else 0
            except:
                precio = 0
            
            # Determinar el estado del producto
            estado = 'disponible'  # Estado por defecto
            try:
                # Buscar indicadores de estado
                if product.find_elements(By.CSS_SELECTOR, '.out-of-stock'):
                    estado = 'agotado'
                elif product.find_elements(By.CSS_SELECTOR, '.discount'):
                    estado = 'oferta'
            except:
                pass  # Mantener estado por defecto si hay error
            
            # Construir objeto de producto
            return {
                'nombre': nombre,
                'precio': precio,
                'categoria': category,
                'subcategoria': subcategory,
                'estado': estado,
                'ultima_actualizacion': datetime.now()
            }
            
        except Exception as e:
            print(f"[ERROR] Error extrayendo información: {str(e)}")
            return None

    def get_products(self):
        products = {}
        
        # Procesar categorías normales
        for category, subcategories in self.categories.items():
            for subcategory in subcategories:
                print(f"\n[INFO] Procesando: {category} - {subcategory}")
                
                try:
                    url = f"{self.base_url}{subcategory}"
                    self.driver.get(url)
                    time.sleep(5)
                    
                    self.scroll_page()
                    
                    product_elements = self.driver.find_elements(By.CSS_SELECTOR, '.product-card')
                    print(f"[INFO] Encontrados {len(product_elements)} productos")
                    
                    for product in product_elements:
                        info = self.extract_product_info(product, category, subcategory.split('/')[-1])
                        if info:
                            products[info['nombre']] = info
                            self.save_product_to_db(info)
                    
                    total_actual = self.productos.count_documents({})
                    print(f"[DB] Total productos en MongoDB: {total_actual}")
                    
                except Exception as e:
                    print(f"[ERROR] Error en categoría {category}: {str(e)}")
                    continue
        
        return products

    def scroll_page(self):
        """Scroll más suave y controlado"""
        try:
            for _ in range(4):
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(2)
        except Exception as e:
            print(f"[WARN] Error durante scroll: {e}")

    def save_product_to_db(self, product):
        """Guardar producto en MongoDB con validación de campos"""
        try:
            # Validar campos requeridos
            required_fields = ['nombre', 'precio', 'categoria', 'subcategoria', 'estado']
            for field in required_fields:
                if field not in product:
                    print(f"[ERROR] Falta campo requerido: {field}")
                    return
            
            # Validar estado
            valid_states = ['disponible', 'agotado', 'oferta']
            if product['estado'] not in valid_states:
                print(f"[ERROR] Estado inválido: {product['estado']}")
                product['estado'] = 'disponible'  # Usar valor por defecto
            
            # Actualizar en MongoDB
            result = self.productos.update_one(
                {'nombre': product['nombre']},
                {
                    '$set': {
                        'nombre': product['nombre'],
                        'precio': product['precio'],
                        'categoria': product['categoria'],
                        'subcategoria': product['subcategoria'],
                        'estado': product['estado'],
                        'ultima_actualizacion': datetime.now()
                    },
                    '$setOnInsert': {'fecha_creacion': datetime.now()}
                },
                upsert=True
            )
            
            if result.upserted_id:
                print(f"[DB] + Producto nuevo: {product['nombre']} ({product['estado']})")
                self.products_saved += 1
            else:
                print(f"[DB] ↻ Producto actualizado: {product['nombre']} ({product['estado']})")
                self.products_updated += 1
                
        except Exception as e:
            print(f"[ERROR] Error guardando en MongoDB: {str(e)}")

    def print_stats(self):
        try:
            total_en_db = self.productos.count_documents({})
            print("\n=== Estadísticas de MongoDB ===")
            print(f"Productos nuevos guardados: {self.products_saved}")
            print(f"Productos actualizados: {self.products_updated}")
            print(f"Total en base de datos: {total_en_db}")
            
            # Mostrar algunos ejemplos de la base de datos
            print("\nÚltimos productos guardados:")
            for doc in self.productos.find().sort("ultima_actualizacion", -1).limit(3):
                print(f"- {doc['nombre']}: ${doc['precio']['valor']}")
                
        except Exception as e:
            print(f"[ERROR] Error obteniendo estadísticas: {e}")

    def close(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        if hasattr(self, 'client'):
            self.client.close()
            print("[INFO] Conexión a MongoDB cerrada")

    def get_element_text(self, element, selectors):
        """Intenta múltiples selectores hasta encontrar uno que funcione"""
        for selector in selectors:
            try:
                result = element.find_element(By.CSS_SELECTOR, selector).text.strip()
                if result:
                    return result
            except:
                continue
        return None

def main():
    print("\n=== Iniciando recolección de productos ===\n")
    scraper = JumboScraper()
    
    try:
        # Recolectar y guardar productos
        products = scraper.get_products()
        
        # Verificar total en MongoDB
        total_en_db = scraper.productos.count_documents({})
        print(f"\n[INFO] Total de productos en MongoDB: {total_en_db}")
        
        # Guardar copia en JSON
        output = {
            'metadata': {
                'fecha_ejecucion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_productos': len(products),
                'total_en_mongodb': total_en_db
            },
            'productos': products
        }
        
        with open('productos.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # Mostrar estadísticas
        scraper.print_stats()
        print(f"Total productos en MongoDB: {total_en_db}")
        
    except Exception as e:
        print(f"[ERROR] Error durante la ejecución: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(line_buffering=True)
        main()
    except Exception as e:
        print(f"[ERROR] Error fatal: {str(e)}")
        sys.exit(1)