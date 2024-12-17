from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urls import collect_all_urls
import logging
import time
import random
import os

def init_database():
    print("\n=== Iniciando proceso de inicialización de base de datos ===\n")
    
    try:
        # Verificar conexión a MongoDB
        print("Conectando a MongoDB...")
        client = MongoClient('mongodb://localhost:27017/')
        db = client['precio_comparador']
        # Verificar conexión
        client.server_info()
        print("✓ Conexión exitosa a MongoDB\n")
        
        # Limpiar colecciones
        print("Limpiando colecciones existentes...")
        db.productos.drop()
        db.urls.drop()
        db.historial_precios.drop()
        print("✓ Colecciones limpiadas exitosamente\n")
        
        # Recolectar URLs
        print("Iniciando recolección de URLs (esto puede tomar varios minutos)...")
        product_urls = collect_all_urls()
        
        if not product_urls:
            raise Exception("No se pudieron recolectar URLs")
        
        print(f"✓ Se recolectaron URLs para {len(product_urls)} productos\n")
        
        # Insertar datos
        print("Insertando productos en la base de datos...")
        productos_insertados = 0
        
        for nombre, datos in product_urls.items():
            try:
                # Insertar producto
                producto = {
                    'id': datos['id'],
                    'nombre': nombre,
                    'imagen': datos['imagen'],
                    'descripcion': datos.get('descripcion', ''),
                    'categoria': datos['categoria']
                }
                db.productos.insert_one(producto)
                
                # Insertar URLs
                urls = {
                    'product_id': datos['id']
                }
                
                # Agregar URLs de cada tienda
                for tienda in ['jumbo', 'lider', 'unimarc', 'tottus', 'acuenta']:
                    if tienda in datos:
                        urls[tienda] = datos[tienda]
                
                db.urls.insert_one(urls)
                productos_insertados += 1
                if productos_insertados % 50 == 0:  # Actualizar cada 50 productos
                    print(f"  Progreso: {productos_insertados} productos insertados")
            except Exception as e:
                print(f"  ⚠ Error insertando producto {nombre}: {str(e)}")
        
        print(f"\n✓ Proceso completado exitosamente")
        print(f"  Total productos insertados: {productos_insertados}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
