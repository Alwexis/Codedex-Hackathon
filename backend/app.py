#Información
#* Nombre del Proyecto: WaveNet
#* Contenedor Imágenes: https://api.imgbb.com/
#* Hosts (posibles): https://railway.app/
#*                   https://render.com/
#*                   https://fly.io/
#*                   https://www.netlify.com/

from fastapi import APIRouter, Depends, FastAPI, Header, File, UploadFile, Response, status, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import socketio
from db import db
from auth import check_if_user_exists, register_user_if_not_exist, get_user_by_email, get_user_by_uid, get_user_by_username
from models import User, _User, Post, Chat, Message
from firebase_admin import auth
from firebase import init_firebase
from bson.json_util import dumps
from util import generate_wavebond, get_wavebond, decrypt_aes, get_user_from_wavebond, upload_image, update_posts_author, get_user_post_likes
import os
from pydantic import BaseModel
from pymongo import DESCENDING, ASCENDING

# Creamos la aplicación FastAPI e inicializamos Firebase
app = FastAPI()
init_firebase()

# Integrar Socket.IO con FastAPI
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)
# sio.attach(app)
# Montamos la aplicación FastAPI en el servidor de Socket.IO
app.mount("/socket.io", socketio.ASGIApp(sio))

# Configurar CORS para aceptar cualquier origen (por ahora, en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#* Middleware
async def get_current_user(response: Response, authorization: Optional[str] = Header(None)):
    #? Revisamos si el token BEARER está presente
    if not authorization or not authorization.startswith("Bearer"):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return { "status": "error", "message": "BEARER Token not found" }

    #? Extraemos el token de la cabecera
    token = authorization.split("Bearer ")[1]
    try:
        #? Verificamos el token con Firebase y además, lo decodificamos para obtener el userid (correo)
        decoded_token = auth.verify_id_token(token, clock_skew_seconds=60)
        uid = decoded_token["uid"]
        return uid
    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return { "status": "error", "message": "BEARER Token not found" }

#* Rutas normales
@app.post("/auth/register")
async def register(user: _User):
    registered = register_user_if_not_exist(user)
    return { "status": "error" if not registered else "success" }

@app.get("/auth/user")
async def user(response: Response, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "User not found." }
    return { "user": user }

@app.patch("/auth/user")
async def user(response: Response, username: str = Form(...), public_profile: bool = Form(...), file: Optional[UploadFile] = File(None), uid: str = Depends(get_current_user)):
    userToUpdate = get_user_by_uid(uid)
    if not userToUpdate:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "User not found." }
    usernameExists = get_user_by_username(username)
    if usernameExists and usernameExists.uid != userToUpdate.uid:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { "status": "error", "message": "Username already exists." }
    #? Si es que NO se recibió un archivo, se mantiene la imagen de perfil actual
    newPfp = userToUpdate.profile_picture if not file else "/no_pfp.webp"
    if file:
        #* Obtenemos los Bytes del archivo y lo subimos a la API de ImgBB con nuestra función auxiliar.
        file_content = await file.read()
        url = upload_image(file_content)
        newPfp = url
    #? Actualizamos los datos del usuario
    userToUpdate.username = username
    userToUpdate.profile_picture = newPfp
    userToUpdate.public_profile = public_profile
    db.users.update_one({ "uid": userToUpdate.uid }, { "$set": userToUpdate.dict() })
    #* Actualizamos los Posts que pertenecen al usuario para que reflejen los cambios.
    #! Actualmente hay una mala práctica, y es que guardamos la instancia de Usuario en cada Post, lo cual puede crear documentos MUY grandes. Esto será cambiado luego.
    update_posts_author(userToUpdate)
    return { "status": "success", "user": userToUpdate }

@app.get("/likes/user")
async def user(response: Response, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "User not found." }
    #* Usamos la función auxiliar para obtener los Likes de los Posts de un Usuario
    likes = get_user_post_likes(user)
    return { "likes": likes }

@app.get("/friends/")
async def user(response: Response, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "User not found." }
    #* Buscamos los Usuarios que son amigos del Usuario actual
    friends = list(db.users.find({ "uid": { "$in": user.friends } }, { "_id": 0 }))
    return { "friends": dumps(friends) }

#* Mensajes
@app.get("/chats/")
async def chat_with_user(response: Response, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    #* Obtenemos los Chats en los cuales esté el usuario actual
    chat = db.chat.find(
        { "users.uid": user.uid },
        { "_id": 0 } 
    )
    if not chat:
        chat = []
    return { "status": "success", "result": dumps(chat) }

@app.get("/messages/{chat_id}")
async def user(response: Response, chat_id: str, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    chat_to_search = db.chat.find_one({ "id": chat_id }, { "_id": 0 })
    if not chat_to_search:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Chat not found." }
    #* Retornamos los mensajes del Chat ordenados por fecha de forma ascendente
    messages = list(db.messages.find({ "chat": chat_id }, { "_id": 0 }).sort("fecha", ASCENDING))
    # messages = list(db.messages.find({ "users": { "$all": [user.uid, userToSearch.uid] } }).sort("fecha", DESCENDING))
    return { "status": "success", "result": dumps(messages) }

#* Posts
@app.get("/posts/")
async def user(response: Response, user: str, uid: str = Depends(get_current_user)):
    selfUser = get_user_by_uid(uid)
    if not selfUser:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    #* Acá corroboramos si es que se solicitó los posts públicos y/o los de amigos y los retornamos en orden descendente
    if user == "public-friends":
        posts = list(db.posts.find({
                    "$or": [
                        { "user.uid": { "$in": selfUser.friends } },
                        { "user.public_profile": True }
                    ]
                }).sort("fecha", DESCENDING))
    else:
        #* En caso de que no, se buscan los posts del usuario solicitado y se retornan en orden descendente
        userToSearch = get_user_by_uid(user)
        if not userToSearch:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { "status": "error", "message": "User not found." }
        posts = list(db.posts.find({"user.uid": userToSearch.uid}).sort("fecha", DESCENDING))
    return { "result": dumps(posts) }

@app.delete("/post/{post_id}")
async def delete_post(response: Response, post_id: str, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    postToDelete = db.posts.find_one({ "id": post_id })
    if not postToDelete:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Post not found." }
    if postToDelete["user"]["uid"] != user.uid:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return { "status": "error", "message": "You can't delete a post that doesn't belong to you." }
    db.posts.delete_one({ "id": post_id })
    return { "status": "success", "message": "Post deleted." }

@app.post("/create-post/")
async def create_post(response: Response, title: str = Form(...), content: str = Form(...), files: Optional[List[UploadFile]] = File(None), uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    #* Iteramos los archivos recibidos y los subimos a la API de ImgBB, luego los adjuntamos al Post a modo de URLs.
    files_urls = []
    if files:
        for file in files:
            file_content = await file.read()
            url = upload_image(file_content)
            files_urls.append(url)
    newPost = Post(title=title, content=content, files=files_urls, user=user)
    createdPost = db.posts.insert_one(newPost.model_dump())
    if not createdPost:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return { "status": "error", "message": "Error creating the post." }
    return { "status": "success", "post": newPost }

#* Cuerpo de Like (body de petición)
class LikeBody(BaseModel):
    type: str #* A futuro, para saber si Likeo un Post, un Comentario o una Respuesta.
    id: str

@app.post("/like/")
async def like(response: Response, body: LikeBody, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    obj = db[body.type].find_one({ "id": body.id }, { "_id": 0 })
    if not obj:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Post not found." }
    if user.uid in obj["likes"]:
        obj["likes"].remove(user.uid)
        like = False
    else:
        obj["likes"].append(user.uid)
        like = True
    db[body.type].update_one({ "id": obj["id"] }, { "$set": { "likes": obj["likes"] } })
    return { "status": "success", "action": "like" if like else "dislike", "object": obj }

#* Wavebond
@app.get("/wavebond/")
async def wavebond(response: Response, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    #* Obtenemos el Wavebond del usuario actual, en caso de que no exista, lo generamos desde cero.
    actual_wavebond = get_wavebond(user)
    generateFromZero = False
    if not actual_wavebond:
        generateFromZero = True
    #* Generamos el Wavebond, lo almacenamos y lo retornamos a modo de archivo.
    file_path = generate_wavebond(user, actual_wavebond, generateFromZero)
    if not os.path.exists(file_path):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return { "status": "error", "message": "Error generating a wavebond." }

    return FileResponse(
        path=file_path,
        filename=f"{user.username}.wavebond",
        media_type="application/octet-stream"
    )

@app.post("/wavebond/", status_code=201)
async def insert_wavebond(response: Response, file: UploadFile, uid: str = Depends(get_current_user)):
    user = get_user_by_uid(uid)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "status": "error", "message": "Invalid session." }
    #* Leemos el contenido del wavebond y obtenemos el usuario al que pertenece con nuestra función auxiliar.
    wavebond_content = await file.read()
    wavebondUser = get_user_from_wavebond(wavebond_content)
    if not wavebondUser:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { "status": "error", "message": "That wavebond is outdated or doesn't belong to anybody." }
    if wavebondUser.uid == user.uid:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { "status": "error", "message": "Sadly, you can't share a wavebond with yourself." }
    if user.uid in wavebondUser.friends:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { "status": "error", "message": "You already share a wavebond with that user." }
    #* Agregamos a ambos usuarios como amigos y creamos un chat entre ellos.
    wavebondUser.friends.append(user.uid)
    user.friends.append(wavebondUser.uid)
    db.users.update_one({ "uid": user.uid }, { "$set": { "friends": user.friends } })
    db.users.update_one({ "uid": wavebondUser.uid }, { "$set": { "friends": wavebondUser.friends } })
    chat = Chat(users=[user, wavebondUser])
    db.chat.insert_one(chat.model_dump())
    return { "status": "success", "wavebond_user": wavebondUser, "updated_user": user }

#* WebSockets Socket.IO
# Diccionario para rastrear usuarios y sus rooms
connected_users = {}
room_users = {}

# Eventos de conexión y desconexión
@sio.event
async def connect(sid, environ):
    #* Agregamos al usuario a la lista de conectados junto con su información
    connected_users[sid] = {"room": None, "uid": None, "email": None, "username": None}
    await sio.emit("message", {"info": f"Usuario conectado: {sid}"}, to=sid)

@sio.event
async def disconnect(sid):
    #* Eliminamos al usuario de la lista de conectados y de su room
    if sid in connected_users:
        room = connected_users[sid]["room"]
        if room:
            sio.leave_room(sid, room)
            room_users[room].remove(sid)
            await sio.emit("message", {"info": f"{sid} salió del room {room}"}, to=room)
            if not room_users[room]:
                del room_users[room]
        del connected_users[sid]

# Evento para unirse a un room
@sio.event
async def join_room(sid, data):
    room = data.get("room")
    uid = data.get("uid")

    if not room or not uid:
        await sio.emit("error", {"error": "Room, UID no especificado"}, to=sid)
        return
    
    if uid in connected_users.values():
        # await sio.emit("error", {"error": "Usuario ya conectado"}, to=sid)
        return

    user = get_user_by_uid(uid)
    if not user:
        await sio.emit("error", {"error": "Usuario no encontrado"}, to=sid)
        return

    if sid not in connected_users:
        await sio.emit("error", {"error": f"SID {sid} no encontrado en connected_users"}, to=sid)
        return

    try:
        #* Lo ingresamos al room.
        sio.enter_room(sid, room)
        connected_users[sid].update({"room": room, "user": user, "email": user.email})
        room_users[room] = room_users.get(room, []) + [sid]
        # await sio.emit("message", {"info": f"{user.username} se unió al room {room}"}, to=room)
    except Exception as e:
        print(f"Error al intentar unirse al room: {e}")
        await sio.emit("error", {"error": f"Error al unirse al room: {str(e)}"}, to=sid)
        return

# Evento para salir de un room
@sio.event
async def leave_room(sid, data):
    room = data.get("room")
    if not room:
        await sio.emit("error", {"error": "Room no especificado"}, to=sid)
        return
    if room not in room_users:
        await sio.emit("room_users", {"room": room, "users": []}, to=sid)
        return
    #* Sacamos al usuario del room
    users_in_room = [
        {
            "uid": connected_users[user]["uid"],
            "email": connected_users[user]["email"],
            "username": connected_users[user]["username"],
        }
        for user in room_users[room]
    ]
    await sio.emit("room_users", {"room": room, "users": users_in_room}, to=sid)

# Evento para enviar mensajes a un room
@sio.event
async def send_message(sid, data):
    room = data.get("room")
    message = data.get("content")
    file_content = data.get("file_content")
    user_uid = data.get("user")
    if not room or not message or not user_uid:
        await sio.emit("error", {"error": "Room o mensaje no especificado"}, to=sid)
        return
    #* En caso de que haya un archivo, lo subimos a ImgBB y obtenemos la URL
    if file_content:
        file_url = upload_image(file_content)
    else:
        file_url = ""
    user = get_user_by_uid(user_uid)
    messageObj = Message(content=str(message), files=file_url, user=user, chat=room)
    #* Enviamos el mensaje a todos los usuarios del room y lo almacenamos en la base de datos.
    await sio.emit("message", {"sender": sid, "message": messageObj.model_dump_json()}, to=room)
    db.messages.insert_one(messageObj.model_dump())
    db.chat.update_one({ "id": room }, { "$set": { "last_message": messageObj.model_dump() } })