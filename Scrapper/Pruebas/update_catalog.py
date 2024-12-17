import schedule
import time
from Scrapper.Pruebas.search_system import SearchSystem

def actualizar_catalogo():
    sistema = SearchSystem()
    sistema.actualizar_catalogo()

def main():
    print("Iniciando sistema de actualización de catálogo...")
    
    # Primera actualización al inicio
    actualizar_catalogo()
    
    # Programar actualizaciones cada 6 horas
    schedule.every(6).hours.do(actualizar_catalogo)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 