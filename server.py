import socket
import sqlite3
import datetime
import threading

#Configuración del socket TCP/IP y Base de Datos.
HOST = "localhost"
PORT = 5000
DB_NAME = "chat.db"

#Candado para evitar que dos clientes escriban en la DB al mismo tiempo.
db_lock = threading.Lock()

#Inicializamos la base de datos y creamos la tabla de mensajes si no existe.
def inicializar_db():
    try:
        conexion = sqlite3.connect(DB_NAME, check_same_thread=False)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conexion.commit()
        return conexion
    except sqlite3.Error as e:
        print(f"Error crítico: Base de datos no accesible. Detalle: {e}")
        return None

#Guardamos el mensaje recibido en la base de datos con la fecha y hora actual y la IP del cliente.
def guardar_mensaje(conexion, contenido, ip_cliente):
    try:
        with db_lock:
            cursor = conexion.cursor()
            fecha_envio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                (contenido, fecha_envio, ip_cliente)
            )
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al guardar en la base de datos: {e}")

#Configuración del socket TCP/IP.
def inicializar_socket():
    try:
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Utilizamos SO_REUSEADDR para permitir reiniciar el servidor sin esperar a que el puerto se libere.
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor_socket.bind((HOST, PORT))
        #Escuchamos conexiones entrantes, con un máximo de 5 clientes.
        servidor_socket.listen(5)
        print(f"Servidor escuchando concurrentemente en {HOST}:{PORT}...")
        return servidor_socket
    except OSError as e:
        print(f"Error: El puerto {PORT} está ocupado. Detalle: {e}")
        return None

#Recibe, procesa y responde los mensajes del cliente.
def manejar_cliente(cliente_socket, ip_cliente, conexion_db):
    print(f"\n[+] Nueva conexión establecida con {ip_cliente}")
    
    while True:
        try:
            datos = cliente_socket.recv(1024)
            if not datos:
                break 

            mensaje = datos.decode('utf-8')
            
            if mensaje.strip().lower() == 'éxito':
                print(f"[-] El cliente {ip_cliente} cerró la sesión con 'éxito'.")
                break

            print(f"[{ip_cliente}] dice: {mensaje}")
            
            guardar_mensaje(conexion_db, mensaje, ip_cliente)

            #Enviamos una respuesta al cliente con la fecha y hora actual.
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            respuesta = f"Mensaje recibido: {timestamp}"
            cliente_socket.send(respuesta.encode('utf-8'))

        except ConnectionResetError:
            print(f"[!] La conexión con {ip_cliente} se perdió.")
            break

    cliente_socket.close()

#Manejamos la conexión con cada cliente en un hilo separado.
def aceptar_conexiones():
    conexion_db = inicializar_db()
    if not conexion_db:
        return

    servidor_socket = inicializar_socket()
    if not servidor_socket:
        return

    try:
        while True:
            cliente_socket, direccion = servidor_socket.accept()
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente_socket, direccion[0], conexion_db))
            hilo_cliente.start()
            
    except KeyboardInterrupt:
        print("\nApagando el servidor...")
    finally:
        servidor_socket.close()
        conexion_db.close()

if __name__ == "__main__":
    aceptar_conexiones()