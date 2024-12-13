#Información
#* Nombre del Proyecto: WaveNet
#* Contenedor Imágenes: https://api.imgbb.com/
#* Hosts: https://railway.app/
#*        https://render.com/
#*        https://fly.io/
#*        https://www.netlify.com/

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

# Crear instancia de Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()

# Integrar Socket.IO con FastAPI
app.mount("/", socketio.ASGIApp(sio))

# Configurar CORS (opcional, pero útil para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diccionario para rastrear usuarios y sus rooms
connected_users = {}

# Eventos de conexión y desconexión
@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")
    connected_users[sid] = {"room": None}  # Asignar room vacío inicialmente
    await sio.emit("message", {"info": f"Usuario conectado: {sid}"}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")
    if sid in connected_users:
        room = connected_users[sid]["room"]
        if room:
            await sio.leave_room(sid, room)
            await sio.emit("message", {"info": f"{sid} salió del room {room}"}, to=room)
        del connected_users[sid]

# Evento para unirse a un room
@sio.event
async def join_room(sid, data):
    room = data.get("room")
    if not room:
        await sio.emit("error", {"error": "Room no especificado"}, to=sid)
        return
    await sio.enter_room(sid, room)
    connected_users[sid]["room"] = room
    print(f"Usuario {sid} se unió al room {room}")
    await sio.emit("message", {"info": f"{sid} se unió al room {room}"}, to=room)

# Evento para salir de un room
@sio.event
async def leave_room(sid, data):
    room = data.get("room")
    if not room:
        await sio.emit("error", {"error": "Room no especificado"}, to=sid)
        return
    await sio.leave_room(sid, room)
    connected_users[sid]["room"] = None
    print(f"Usuario {sid} salió del room {room}")
    await sio.emit("message", {"info": f"{sid} salió del room {room}"}, to=room)

# Evento para enviar mensajes a un room
@sio.event
async def send_message(sid, data):
    room = data.get("room")
    message = data.get("message")
    if not room or not message:
        await sio.emit("error", {"error": "Room o mensaje no especificado"}, to=sid)
        return
    print(f"Mensaje recibido en room {room}: {message}")
    await sio.emit("message", {"sender": sid, "message": message}, to=room)
