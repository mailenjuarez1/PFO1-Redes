# PFO 1: Chat Cliente-Servidor con Sockets y Base de Datos en Python

Un sistema de chat en red local donde varios clientes pueden conectarse al servidor al mismo tiempo. El servidor guarda el historial en una base de datos y le confirma al usuario cada recepción.

## Características 📌
* **Conexión simultánea:** Varios usuarios pueden chatear a la vez sin bloquearse gracias al uso de hilos (`threading`).
* **Respuesta del servidor:** Cada vez que el servidor recibe y guarda un mensaje, le devuelve al cliente una confirmación con la fecha y hora exacta (ej. `Servidor responde -> Mensaje recibido: 2026-09-20 01:08:51`).
* **Historial guardado:** Todo se almacena automáticamente en un archivo local `chat.db` usando SQLite. No requiere instalar servidores extra.

## Cómo ejecutarlo 💻

1. Abre una terminal en la carpeta del proyecto y arranca el servidor:
   ```bash
   py server.py
   py client.py
