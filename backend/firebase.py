import firebase_admin
from firebase_admin import credentials

# Inicializa Firebase Admin con tus credenciales
def init_firebase():
    cred = credentials.Certificate('/etc/secrets/wavenet-73cf7-firebase-adminsdk-ei1f5-0f2d01c481.json')
    firebase_admin.initialize_app(cred)