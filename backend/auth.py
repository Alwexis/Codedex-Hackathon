from db import db
from models import User

def get_user_by_uid(uid):
    user = db.users.find_one({ 'uid': uid }, { '_id': 0 })
    print(user)
    return user

def get_user_by_username(username):
    user = db.users.find_one({ 'username': username })
    return user

def get_user_by_email(email):
    user = db.users.find_one({ 'email': email })
    return user

def check_if_user_exists(uid, email, username):
    user = db.users.find_one({
        '$or': [
            { 'uid': uid },
            { 'email': email },
            { 'username': username }
        ]
    })
    return user is not None

def register_user_if_not_exist(user):
    if not check_if_user_exists(user.uid, user.email, user.username):
        print("Registrando usuario...")
        _user = User(
            uid=user.uid,
            username=user.username,
            email=user.email,
            secret=user.secret,
            friends=[],
            profile_picture="no_pfp.webp"
        )
        db.users.insert_one(_user.model_dump())
        return True
    return False