import os
import sys
import subprocess

def configure_environment():
    os.environ['PYTHONWARNINGS'] = 'ignore'
    os.environ['WDM_LOG_LEVEL'] = '0'

def run_script(script_name):
    # Obtener la ruta absoluta al directorio Scrapper
    scrapper_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(scrapper_dir, script_name)
    
    print(f"\n=== Ejecutando {script_name} ===\n")
    
    try:
        # Ejecutar el script y capturar tanto stdout como stderr
        process = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Mostrar la salida
        if process.stdout:
            print(process.stdout)
            
        return 0
        
    except subprocess.CalledProcessError as e:
        print("❌ Error ejecutando el script:")
        if e.stdout:
            print("\nSalida estándar:")
            print(e.stdout)
        if e.stderr:
            print("\nSalida de error:")
            print(e.stderr)
        return e.returncode
    
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return 1

def main():
    configure_environment()
    
    print("¿Qué deseas ejecutar?")
    print("1. Recolectar URLs (urls.py)")
    print("2. Inicializar base de datos (init_db.py)")
    print("3. Actualizar precios (update_prices.py)")
    print("4. Ejecutar servidor API (scraperapp.py)")
    
    choice = input("\nIngresa el número de tu elección (1-4): ")
    
    scripts = {
        '1': 'urls.py',
        '2': 'init_db.py',
        '3': 'update_prices.py',
        '4': 'scraperapp.py'
    }
    
    if choice in scripts:
        exit_code = run_script(scripts[choice])
        if exit_code != 0:
            print(f"\n❌ El script terminó con errores (código {exit_code})")
        else:
            print("\n✓ Script ejecutado exitosamente")
    else:
        print("\n❌ Opción no válida")

if __name__ == "__main__":
    main() 