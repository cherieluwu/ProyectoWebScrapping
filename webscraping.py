import requests
from bs4 import BeautifulSoup

url = 'https://www.jumbo.cl/busqueda?ft=aceite'

try:
    response = requests.get(url)
    response.raise_for_status()  # Lanza un error si la respuesta fue mala
    soup = BeautifulSoup(response.text, 'html.parser')


# Extraer todas las clases
    for div in soup.find_all('div'):
        classes = div.get('class')
        if classes:
            print(classes)
        

 # Posibles clases para el nombre del producto
    nombre_clases = [
        'product-container-title',
        'product-brand-wrap',
        'pdp-left-content'
    ]

    # Buscar el nombre del producto
    nombre = 'Nombre no disponible'
    for clase in nombre_clases:
        elemento = soup.find('div', class_=clase)
        if elemento:
            nombre = elemento.text.strip()
            break  # Salir del bucle si se encuentra el nombre

    # Posibles clases para el precio del producto
    precio_clases = [
        'sticky-product-prices',
        'prices-and-controls',
        'price',
        'product-price',
        'current-price',
        'price-label',
        'product-price-wrapper',
        'price-and-availability',
        'price-value',               
        'product-price-value',       
        'current-price-value',       
        'final-price',               
        'discount-price',              
        'price-tag',
        "prices-main-price"                 
        'price-container',           
        'product-price-container'     
    ]

    # Buscar el precio del producto
    precio = 'Precio no disponible'
    for clase in precio_clases:
        elemento = soup.find('div', class_=clase)
        if elemento:
            precio = elemento.text.strip()
            break  # Salir del bucle si se encuentra el precio

    print(f'Nombre: {nombre}, Precio: {precio}')

except requests.exceptions.RequestException as e:
    print(f'Error al realizar la solicitud: {e}')