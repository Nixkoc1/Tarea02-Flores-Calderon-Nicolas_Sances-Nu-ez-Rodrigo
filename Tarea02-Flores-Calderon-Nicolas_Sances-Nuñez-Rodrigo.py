import getopt  # Biblioteca para procesar los argumentos de línea de comandos.
import sys  # Biblioteca para manejar las salidas del sistema y otros aspectos del entorno.
import requests  # Biblioteca para realizar solicitudes HTTP a una API.
import subprocess  # Biblioteca para ejecutar comandos del sistema desde Python.
import time  # Biblioteca para medir el tiempo, en este caso, el tiempo de respuesta.

# Función en la cual consulta el fabricante de una dirección MAC usando la API pública
def consultar_mac(mac_address):
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"
    
    start_time = time.time()  # Inicia el cronómetro para determinar el tiempo de respuesta
    response = requests.get(url)
    end_time = time.time()  # Termina el cronómetro donde determinamos el tiempo de respuesta
    
    response_time = end_time - start_time  # Calcula el tiempo de respuesta
    
    if response.status_code == 200:
        data = response.json()
        return data.get('company', 'Fabricante no encontrado'), response_time
    else:
        return 'Error en la consulta a la API', response_time

# Función para obtener la tabla ARP en el sistema
def obtener_tabla_arp():
    try:
        # Comando en el cual se obtiene la tabla ARP
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return 'Error al obtener la tabla ARP'
    except Exception as e:
        return f'Error al ejecutar el comando ARP: {str(e)}'

# Función principal que procesa los parámetros de entrada
def main(argv):
    mac_address = None
    show_arp = False

    # Procesa los argumentos de línea de comandos, aceptando las opciones --mac, --arp y --help.
    try:
        opts, args = getopt.getopt(argv, "", ["mac=", "arp", "help"])
    except getopt.GetoptError:
        print('Uso incorrecto de los parámetros. Ingresa: OUILookup --mac <mac> | --arp | [--help]')
        sys.exit(2)
    
    # Recorre las opciones ingresadas por el usuario.
    for opt, arg in opts:
        if opt == '--mac':
            mac_address = arg
        elif opt == '--arp':
            show_arp = True
        elif opt == '--help':
            print("Uso: OUILookup --mac <mac> | --arp | [--help]")
            sys.exit()

    # Si se ha proporcionado una dirección MAC, realiza la consulta a la API.
    if mac_address:
        fabricante, tiempo_respuesta = consultar_mac(mac_address)
        print(f"MAC address : {mac_address}\nFabricante : {fabricante}\nTiempo de respuesta: {tiempo_respuesta:.2f} segundos")
    elif show_arp:
        arp_output = obtener_tabla_arp()
        print("Tabla ARP:\n", arp_output)
    else:
        print("Debes colocar --mac o --arp. O sino utiliza --help para encontrar más información.")
        sys.exit(2)

# Punto de entrada del programa
if __name__ == "__main__":
    main(sys.argv[1:])
