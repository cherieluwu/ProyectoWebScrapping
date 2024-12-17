import requests
from bs4 import BeautifulSoup
from .base_scraper import ScraperSupermercado

class ScraperSantaIsabel(ScraperSupermercado):
    def obtener_precio(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar el precio en los metadatos
            precio_meta = soup.find('meta', {'property': 'product:price:amount'})
            if precio_meta:
                precio = precio_meta.get('content')
                return f"${precio}"
            return "Precio no encontrado en Santa Isabel"
            
        except requests.exceptions.RequestException as e:
            return f'Error en Santa Isabel: {e}'
