from pymongo import MongoClient

def reset_database():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['precio_comparador']
    db.productos.drop()
    print("Base de datos reiniciada")

if __name__ == "__main__":
    reset_database() 