from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from pymongo import DESCENDING, ASCENDING

from flask import current_app, g
from werkzeug.local import LocalProxy

from project.models import User


def get_db():
    """
    Método de configuración para obtener una instancia de db
    """
    db = getattr(g, "_database", None)

    PIALARA_DB_URI = current_app.config["PIALARA_DB_URI"]
    PIALARA_DB_DB_NAME = current_app.config["PIALARA_DB_NAME"]

    if db is None:
        db = g._database = MongoClient(
            PIALARA_DB_URI,
            maxPoolSize=50,
            timeoutMS=2500
        )[PIALARA_DB_DB_NAME]
    return db


# Utilizamos LocalProxy para leer la variable global usando sólo db
db = LocalProxy(get_db)


def get_all_users():
    """
    Devuelve una lista con todos los usuarios del sistema
    """
    try:
        return list(db.users.find({}).sort("nombre", ASCENDING))
    except Exception as e:
        return e


def get_user_by_id(id):
    """
    Devuelve un objeto User a partir de su id
    """
    try:
        usuario = db.users.find_one({"_id": ObjectId(id)})

        usuario_obj = User(id=usuario["_id"],
                           email=usuario.get("email"),
                           nombre=usuario.get("nombre"),
                           password=usuario.get("password"),
                           rol=usuario.get("rol"),
                           parent=usuario.get("parent"),
                           sexo=usuario.get("sexo"),
                           patologia=usuario.get("patologia"),
                           fecha_nac=usuario.get("fecha_nac"),
                           edad=usuario.get('edad'))
        print("usuario_obj por id:", usuario_obj)
        return usuario_obj
    except Exception as e:
        return e


def get_users(rol):
    """
    Devuelve una lista con los usuarios de un determinado rol
    """
    try:
        return list(db.users.find({"rol": rol}))
    except Exception as e:
        return e


def get_child_users_by_email(email):
    """
    Devuelve una lista con los usuarios cuyo padre contenga determinado email
    """
    try:
        return list(db.users.find({"parent": email}))
    except Exception as e:
        return e


def get_user(email):
    """
    Devuelve un objeto User
    Método a emplear en el login
    """
    try:
        usuario = db.users.find_one({"email": email})

        usuario_obj = User(id=usuario["_id"],
                           email=usuario.get("email"),
                           nombre=usuario.get("nombre"),
                           password=usuario.get("password"),
                           rol=usuario.get("rol"),
                           parent=usuario.get("parent"))
        print("Usuario objeto por email:", usuario_obj)

        return usuario_obj
    except Exception as e:
        print("Se ha producido un error", e)
        return None


def insert_user(user):
    """
    Inserta un usuario en la base de datos
    """
    try:
        if user.rol == 'Cliente':
            doc = {"email": user.email,
                   "password": user.password,
                   "nombre": user.nombre,
                   "rol": user.rol,
                   "parent": user.parent,
                   "sexo": user.sexo,
                   "patologia": user.patologia,
                   "fecha_nac": user.fecha_nac,
                   "edad": user.edad,
                   "tecnico": user.tecnico}
        else:
            doc = {"email": user.email,
                   "password": user.password,
                   "nombre": user.nombre,
                   "rol": user.rol,
                   "parent": user.parent}

        return db.users.insert_one(doc)
    except Exception as e:
        return e


def update_user(user):
    """
    Modifica un usuario (sólo atributos básicos)
    """
    try:
        if user.rol == 'Cliente':
            expr = {"$set": {"nombre": user.nombre, "email": user.email, "rol": user.rol, "fecha_nac": user.fecha_nac, "patologia": user.patologia, "sexo": user.sexo, "edad": user.edad}}
        else:
            expr = {"$set": {"nombre": user.nombre, "email": user.email, "rol": user.rol}}

        return db.users.update_one({"_id": ObjectId(user.id)}, expr)
    except Exception as e:
        return e


def delete_user(id):
    """
    Elimina un usuario por su id
    """
    try:
        return db.users.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        return e
