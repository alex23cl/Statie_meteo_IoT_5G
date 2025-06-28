import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("weather-e95f2-firebase-adminsdk-fbsvc-d10785bb38.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
