from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import random
import requests

class BaseScraper(ABC):
    def __init__(self):
        # Configuración de Selenium con Chrome en modo headless
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def _wait_and_get_element(self, selector, by=By.CSS_SELECTOR):
        try:
            return self.wait.until(EC.presence_of_element_located((by, selector)))
        except TimeoutException:
            return None

    @abstractmethod
    def obtener_precio(self, url):
        pass

class ScraperJumbo(BaseScraper):
    def obtener_precio(self, url):
        try:
            self.driver.get(url)
            # Esperar por el elemento de precio en Jumbo
            precio_elem = self._wait_and_get_element('.product-price')
            if precio_elem:
                return precio_elem.text.strip()
            return None
        except Exception as e:
            print(f"Error en Jumbo: {str(e)}")
            return None

class ScraperLider(BaseScraper):
    def obtener_precio(self, url):
        try:
            self.driver.get(url)
            # Esperar por el elemento de precio en Lider
            precio_elem = self._wait_and_get_element('.price-container .price')
            if precio_elem:
                return precio_elem.text.strip()
            return None
        except Exception as e:
            print(f"Error en Lider: {str(e)}")
            return None

class ScraperUnimarc(BaseScraper):
    def obtener_precio(self, url):
        try:
            self.driver.get(url)
            # Esperar por el elemento de precio en Unimarc
            precio_elem = self._wait_and_get_element('.product-price')
            if precio_elem:
                return precio_elem.text.strip()
            return None
        except Exception as e:
            print(f"Error en Unimarc: {str(e)}")
            return None

# Agregar más scrapers siguiendo el mismo patrón
class ScraperTottus(BaseScraper):
    def obtener_precio(self, url):
        try:
            self.driver.get(url)
            precio_elem = self._wait_and_get_element('.product-price')
            if precio_elem:
                return precio_elem.text.strip()
            return None
        except Exception as e:
            print(f"Error en Tottus: {str(e)}")
            return None

class ScraperAcuenta(BaseScraper):
    def obtener_precio(self, url):
        try:
            self.driver.get(url)
            precio_elem = self._wait_and_get_element('.price-box .price')
            if precio_elem:
                return precio_elem.text.strip()
            return None
        except Exception as e:
            print(f"Error en Acuenta: {str(e)}")
            return None
    
    def buscar_productos(self, query):
        url = f"https://www.lider.cl/supermercado/search?query={query}"
        html = self._get_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        productos = []
        
        # Ajustar selectores según la estructura de la página
        for item in soup.select('.product-item'):
            try:
                productos.append({
                    'nombre': item.select_one('.product-title').text.strip(),
                    'precio': self._extraer_precio(item.select_one('.price').text),
                    'url': 'https://www.lider.cl' + item.select_one('a')['href'],
                    'imagen': item.select_one('img')['src'],
                    'tienda': 'lider'
                })
            except Exception as e:
                print(f"Error procesando producto Lider: {str(e)}")
        
        return productos
    
    def _extraer_precio(self, texto):
        return ''.join(filter(str.isdigit, texto))
    
    def _get_page(self, url):
        """Obtiene el contenido de una página con reintentos"""
        for _ in range(3):  # 3 intentos
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"Error obteniendo {url}: {str(e)}")
                time.sleep(random.uniform(1, 3))
        return None

class ScraperTrebol(BaseScraper):
    # Implementación similar
    pass

class ScraperMercadoLibre(BaseScraper):
    def buscar_productos(self, query):
        url = f"https://listado.mercadolibre.cl/{query}_CategoryID_FOOD_AND_DRINKS"
        # Implementación específica para MercadoLibre
        pass 