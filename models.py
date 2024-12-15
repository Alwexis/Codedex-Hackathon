from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class _User(BaseModel):
    uid: str
    username: str
    email: str
    profile_picture: str = Field(default="/no_pfp.webp")
    public_profile: bool = False

class User(BaseModel):
    uid: str
    username: str
    email: str
    friends: list[str] = Field(default=[]) # lista con las IDs de los amigos
    profile_picture: str = Field(default="/no_pfp.webp")
    public_profile: bool = False

class CommentaryResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    fecha: datetime = Field(default_factory=datetime.now)
    content: str
    files: list[str] # lista con las URLs de los archivos adjuntos
    user: User
    likes: list[str] # lista con las IDs de los usuarios que han dado like

class Commentary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    fecha: datetime = Field(default_factory=datetime.now)
    content: str
    files: list[str] # lista con las URLs de los archivos adjuntos
    user: User
    likes: list[str] # lista con las IDs de los usuarios que han dado like
    responses: list[str] # lista con las IDs de los comentarios de respuesta

class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    fecha: datetime = Field(default_factory=datetime.now)
    title: str
    content: str
    files: list[str] # lista con las URLs de los archivos adjuntos
    user: User
    likes: list[str] = Field(default=[]) # lista con las IDs de los usuarios que han dado like
    comments: list[Commentary] = Field(default=[]) # lista con los comentarios del post
    pinned: bool = Field(default=False)

class Wavebond(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    fecha: datetime = Field(default_factory=datetime.now)
    user: str # ID del usuario
    wave: bytes # hash generado con la función generate_wavebond
    version: float = 0.1

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    fecha: datetime = Field(default_factory=datetime.now)
    content: str
    files: str # URL de los archivos adjuntos
    user: User
    chat: str # ID del chat

class Chat(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    fecha: datetime = Field(default_factory=datetime.now)
    users: list[User] # lista con las IDs de los usuarios que participan en el chat
    messages: list[str] = Field(default=[]) # lista con las IDs de los mensajes del chat
    last_message: Message = Field(default=None) # Último mensaje enviado