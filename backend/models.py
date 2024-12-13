from pydantic import BaseModel

class User(BaseModel):
    uid: str
    username: str
    email: str
    secret: str
    friends: List[str] # Lista con las IDs de los amigos
    profile_picture: str

class CommentaryResponse(BaseModel):
    id: str
    content: str
    files: List[str] # Lista con las URLs de los archivos adjuntos
    user: User
    likes: List[str] # Lista con las IDs de los usuarios que han dado like

class Commentary(BaseModel):
    id: str
    content: str
    files: List[str] # Lista con las URLs de los archivos adjuntos
    user: User
    likes: List[str] # Lista con las IDs de los usuarios que han dado like
    responses: List[str] # Lista con las IDs de los comentarios de respuesta

class Post(BaseModel):
    id: str
    title: str
    content: str
    files: List[str] # Lista con las URLs de los archivos adjuntos
    user: User
    likes: List[str] # Lista con las IDs de los usuarios que han dado like
    comments: List[Commentary] # Lista con los comentarios del post