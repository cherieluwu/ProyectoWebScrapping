from pymongo import MongoClient
from pprint import pprint

def verificar_datos():
    # Conectar a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['precio_comparador']
    
    # Verificar cantidad de productos
    total_productos = db.productos.count_documents({})
    print(f"\nTotal de productos en la base de datos: {total_productos}")
    
    # Mostrar productos por tienda
    for tienda in ['lider', 'jumbo', 'santaisabel', 'unimarc', 'acuenta', 'trebol']:
        count = db.productos.count_documents({'tienda': tienda})
        print(f"Productos en {tienda}: {count}")
    
    # Mostrar algunos ejemplos de productos
    print("\nEjemplos de productos guardados:")
    for producto in db.productos.find().limit(5):
        pprint(producto)
    
    # Verificar últimas actualizaciones
    print("\nÚltimas actualizaciones:")
    for producto in db.productos.find().sort('ultima_actualizacion', -1).limit(3):
        print(f"Producto: {producto['nombre']}")
        print(f"Tienda: {producto['tienda']}")
        print(f"Precio: ${producto['precio']}")
        print(f"Actualizado: {producto['ultima_actualizacion']}")
        print("---")

if __name__ == "__main__":
    verificar_datos() 