import requests
from bs4 import BeautifulSoup
from .base_scraper import ScraperSupermercado

class ScraperJumbo(ScraperSupermercado):
    def obtener_precio(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            precio_elemento = soup.find('span', {'class': 'prices-main-price', 'id': 'scraping-tmp'})
            if precio_elemento:
                return precio_elemento.text.strip()
            return "Precio no encontrado en Jumbo"
            
        except requests.exceptions.RequestException as e:
            return f'Error en Jumbo: {e}'