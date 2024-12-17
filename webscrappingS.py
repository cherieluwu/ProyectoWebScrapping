from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configura Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL de la página a raspar
url = 'https://www.jumbo.cl/busqueda?ft=aceite'
driver.get(url)


# Espera a que se cargue la página y busca el nombre y el precio
nombre = driver.find_element("class name", "product-container-title").text
precio = driver.find_element("class name", "sticky-product-prices").text

print(f'Nombre: {nombre}, Precio: {precio}')

# Cierra el navegador
driver.quit()