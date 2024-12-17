import requests
from bs4 import BeautifulSoup
import json
from .base_scraper import ScraperSupermercado

class ScraperUnimarc(ScraperSupermercado):
    def obtener_precio(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tags = soup.find_all('script', {'type': 'application/ld+json'})
            
            for script in script_tags:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and 'offers' in data:
                        return data['offers']['price']
                except json.JSONDecodeError:
                    continue
                    
            return "Precio no encontrado en Unimarc"
            
        except requests.exceptions.RequestException as e:
            return f'Error en Unimarc: {e}'