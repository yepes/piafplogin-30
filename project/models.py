from flask_login import UserMixin


class User(UserMixin):
    edad = ''

    def __init__(self, id, email, nombre, password, rol, parent="", sexo="", patologia="", fecha_nac="", edad="", tecnico=""):
        self.id = id
        self.email = email
        self.nombre = nombre
        self.password = password
        self.rol = rol
        self.parent = parent
        self.sexo = sexo
        self.patologia = patologia
        self.fecha_nac = fecha_nac
        self.edad = edad
        self.tecnico = tecnico

    def __str__(self):
        return f"{self.email} ({self.nombre} / {self.password})"
