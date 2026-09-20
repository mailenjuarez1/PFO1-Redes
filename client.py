import socket

#Configuración del socket TCP/IP
HOST = "localhost"
PORT = 5000

#Inicializamos el socket bajo el modelo Cliente-Servidor.
def iniciar_cliente():
    
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #Conectamos el socket del cliente al servidor.
        cliente_socket.connect((HOST, PORT))
        print(f"Conectado exitosamente al servidor {HOST}:{PORT}")
        print("----Iniciando el chat----")
        print("Escribí tus mensajes. Para salir del chat, escribí 'éxito'.")

        while True:
            #Enviamos el mensaje ingresado por el usuario al servidor.
            mensaje = input("\nTú: ")

            if not mensaje.strip():
                continue

            cliente_socket.send(mensaje.encode('utf-8'))

            if mensaje.strip().lower() == 'éxito':
                print("Cerrando la aplicación cliente...")
                break

            #Mostramos la respuesta del servidor en la consola del cliente.
            respuesta_servidor = cliente_socket.recv(1024).decode('utf-8')
            print(f"Servidor responde -> {respuesta_servidor}")

    except ConnectionRefusedError:
        print("Error crítico: Servidor no disponible. Verificá que server.py esté en ejecución.")
    finally:
        cliente_socket.close()

if __name__ == "__main__":
    iniciar_cliente()