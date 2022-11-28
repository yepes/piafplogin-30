from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

DB_URI = config['PROD']['PIALARA_DB_URI']
DB_NAME = config['PROD']['PIALARA_DB_NAME']
# DB_URI = config['LOCAL']['PIALARA_DB_URI']
# DB_NAME = config['LOCAL']['PIALARA_DB_NAME']

db = MongoClient(DB_URI)[DB_NAME]

usuarios = [
    {"nombre":"Admin", "email":"admin@admin.com", "password":generate_password_hash("admin", method='sha256'), "rol":"Administrador"},
    {"nombre":"Admin2", "email":"admin2@admin.com", "password":generate_password_hash("admin", method='sha256'), "rol":"Administrador"},
    {"nombre":"Alumno", "email":"alumno@alumno.com", "password":generate_password_hash("alumno", method='sha256'), "rol":"Técnico"},
    {"nombre":"Alumno2", "email":"alumno2@alumno.com", "password":generate_password_hash("alumno", method='sha256'), "rol":"Técnico"},
    {"nombre":"Severo Ochoa", "email":"s8a@s8a.com", "password":generate_password_hash("s8a", method='sha256'), "rol":"Cliente", "parent":"alumno@alumno.com"},
    {"nombre":"Antonio Sequeros", "email":"antonioa@sequeros.com", "password":generate_password_hash("sequeros", method='sha256'), "rol":"Cliente", "parent":"alumno2@alumno.com"},
]

try:
    db.users.insert_many(usuarios)
except Exception as e:
    print(e)

