from db import db
from models import User

def get_user_by_uid(uid):
    #* Buscamos el usuario por su UID
    user = db.users.find_one({ 'uid': uid }, { '_id': 0 })
    return User(**user) if user else None

def get_user_by_username(username):
    #* Buscamos el usuario por su username
    user = db.users.find_one({ 'username': username })
    return User(**user) if user else None

def get_user_by_email(email):
    #* Buscamos el usuario por su email
    user = db.users.find_one({ 'email': email })
    return User(**user) if user else None

def check_if_user_exists(uid, email, username):
    #* Corroboramos si el usuario existe
    user = db.users.find_one({
        '$or': [
            { 'uid': uid },
            { 'email': email },
            { 'username': username }
        ]
    })
    return User(**user) if user else None

def register_user_if_not_exist(user):
    #* Registramos al usuario si no existe
    if not check_if_user_exists(user.uid, user.email, user.username):
        print("Registrando usuario...")
        _user = User(
            uid=user.uid,
            username=user.username,
            email=user.email,
            friends=[],
            profile_picture="no_pfp.webp"
        )
        db.users.insert_one(_user.model_dump())
        return True
    return False