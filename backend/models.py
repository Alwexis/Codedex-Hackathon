from pydantic import BaseModel

class _User(BaseModel):
    uid: str
    username: str
    email: str
    secret: str

class User(BaseModel):
    uid: str
    username: str
    email: str
    secret: str
    friends: list[str] # lista con las IDs de los amigos
    profile_picture: str

class CommentaryResponse(BaseModel):
    id: str
    content: str
    files: list[str] # lista con las URLs de los archivos adjuntos
    user: User
    likes: list[str] # lista con las IDs de los usuarios que han dado like

class Commentary(BaseModel):
    id: str
    content: str
    files: list[str] # lista con las URLs de los archivos adjuntos
    user: User
    likes: list[str] # lista con las IDs de los usuarios que han dado like
    responses: list[str] # lista con las IDs de los comentarios de respuesta

class Post(BaseModel):
    id: str
    title: str
    content: str
    files: list[str] # lista con las URLs de los archivos adjuntos
    user: User
    likes: list[str] # lista con las IDs de los usuarios que han dado like
    comments: list[Commentary] # lista con los comentarios del post