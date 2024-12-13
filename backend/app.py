#Información
#* Nombre del Proyecto: WaveNet
#* Contenedor Imágenes: https://api.imgbb.com/
#* Hosts: https://railway.app/
#*        https://render.com/
#*        https://fly.io/
#*        https://www.netlify.com/

from email.header import Header
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import socketio
from db import db
from auth import check_if_user_exists, register_user_if_not_exist, get_user_by_email, get_user_by_uid, get_user_by_username
from models import User, _User
from firebase_admin import auth
from firebase import init_firebase

# Crear instancia de Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()
init_firebase()

# Integrar Socket.IO con FastAPI
app.mount("/ws", socketio.ASGIApp(sio))

# Configurar CORS (opcional, pero útil para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#* Middleware
async def get_current_user(authorization: Optional[str] = Header(None)):
    #? Revisamos si el token BEARER está presente
    if not authorization or not authorization.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Token BEARER no encontrado")
    #? Extraemos el token de la cabecera
    token = authorization.split("Bearer ")[1]
    try:
        #? Verificamos el token con Firebase y además, lo decodificamos para obtener el userid (correo)
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
        return uid
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token BEARER inválido")

#* Rutas normales
@app.post("/auth/register")
async def register(user: _User):
    registered = register_user_if_not_exist(user)
    return { "status": "error" if not registered else "success" }

@app.get("/auth/user")
async def user(uid: str = Depends(get_current_user)):
    print(uid)
    user = get_user_by_uid(uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return { "user": user }

#* WebSockets Socket.IO
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
