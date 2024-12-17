from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['taller']
productos = db['productos']

# Intentar insertar un documento de prueba
test_doc = {"test": True, "mensaje": "Prueba de conexión"}
result = productos.insert_one(test_doc)

# Verificar que se guardó
saved_doc = productos.find_one({"_id": result.inserted_id})
print("Documento guardado:", saved_doc)

# Limpiar el documento de prueba
productos.delete_one({"_id": result.inserted_id})

# Cerrar conexión
client.close()