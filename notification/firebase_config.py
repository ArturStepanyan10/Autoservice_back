import firebase_admin
from firebase_admin import credentials

from AutoService import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
