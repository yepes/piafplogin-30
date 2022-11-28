from datetime import date, datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db, models
from .models import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html')


@main.route('/user_list')
@login_required
def user_list():
    logged_rol = current_user.rol
    if logged_rol == "Administrador":
        users = db.get_all_users()
    else:
        raise Exception("Operación no permitida para el rol", logged_rol)

    return render_template('user_list.html', users=users)


@main.route('/client_list')
@login_required
def client_list():
    logged_rol = current_user.rol
    if logged_rol == "Técnico":
        logged_email = current_user.email
        users = db.get_child_users_by_email(email=logged_email)
    else:
        raise Exception("Operación no permitida para el rol", logged_rol)

    return render_template('client_list.html', users=users)


@main.route('/user_create')
@login_required
def user_create():
    tecnicos = []
    logged_rol = current_user.rol
    if logged_rol == "Administrador":
        tecnicos = db.get_users('Técnico')

    for tecnico in tecnicos:
        print(tecnico)

    return render_template('user_create.html', tecnicos=tecnicos)


@main.route('/user_create', methods=['POST'])
@login_required
def user_create_post():
    email = request.form.get('email')
    nombre = request.form.get('nombre')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    rol = request.form.get('rol')
    tecnico = request.form.get('tecnico')
    sexo = request.form.get('sexo')
    patologia = request.form.get('patologia')
    fechaNacimiento = request.form.get('fechaNacimiento')

    user = db.get_user(email)

    if password1 != password2:
        flash("Las contraseñas no coinciden", "error")
        return redirect(url_for('main.user_create'))

    if user:  # if a user is found, we want to redirect back to user_create page so user can try again
        flash('El email ya está siendo utilizado por otro usuario', "error")
        return redirect(url_for('main.user_create'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    user = models.User(
        id=None,
        email=email,
        nombre=nombre,
        password=generate_password_hash(password1, method='sha256'),
        rol=rol,
        tecnico=tecnico,
        sexo=sexo,
        patologia=patologia,
        fecha_nac=fechaNacimiento
    )

    # añadimos el usuario a la base de datos
    result = db.insert_user(user)
    print("Usuario creado correctamente", result.inserted_id, result.acknowledged)

    return redirect(url_for('main.user_list'))


@main.route('/client_create')
@login_required
def client_create():
    return render_template('client_create.html')


@main.route('/client_create', methods=['POST'])
@login_required
def client_create_post():
    email = request.form.get('email')
    nombre = request.form.get('nombre')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    rol = "Cliente"
    parent = current_user.email
    sexo = request.form.get('sexo')
    patologia = request.form.get('patologia')
    fecha_nac = request.form.get('fecha_nac')

    user = db.get_user(email)

    if password1 != password2:
        flash(f"Las contraseñas no coinciden {password1} {password2}", "error")
        return redirect(url_for('main.client_create'))

    if user:  # if a user is found, we want to redirect back to user_create page so user can try again
        flash('Ya existe un usuario con dicho email', "error")
        return redirect(url_for('main.client_create'))

    today = date.today()
    fecha_nac = datetime.strptime(user.fecha_nac, '%Y-%m-%d')
    user.edad = today.year - fecha_nac.year - ((today.month, today.day) < (fecha_nac.month, fecha_nac.day))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = models.User(id=None, email=email, nombre=nombre,
                           password=generate_password_hash(password1, method='sha256'), sexo=sexo, fecha_nac=fecha_nac,
                           patologia=patologia, rol=rol, parent=parent, edad=fecha_nac)

    # añadimos el usuario a la base de datos
    result = db.insert_user(new_user)
    print("Usuario creado", result.inserted_id, result.acknowledged)

    return redirect(url_for('main.client_list'))


@main.route('/user_view/<string:id>')
@login_required
def user_view(id):
    print("Recuperando usuario por id:", id)
    user = db.get_user_by_id(id)
    return render_template('user_view.html', user=user)


@main.route('/client_view/<string:id>')
@login_required
def client_view(id):
    print("Recuperando usuario por id:", id)
    user = db.get_user_by_id(id)
    return render_template('client_view.html', user=user)


@main.route('/user_edit/<string:id>')
@login_required
def user_edit(id):
    print("Recuperando usuario por id:", id)
    user = db.get_user_by_id(id)
    return render_template('user_edit.html', user=user)


@main.route('/client_edit/<string:id>')
@login_required
def client_edit(id):
    print("Recuperando cliente por id:", id)
    user = db.get_user_by_id(id)
    return render_template('client_edit.html', user=user)


@main.route('/user_edit', methods=['POST'])
@login_required
def user_edit_post():
    id = request.form.get('id')
    email = request.form.get('email')
    nombre = request.form.get('nombre')
    rol = request.form.get('rol')

    user = db.get_user_by_id(id)

    if user.id:
        if nombre:
            user.nombre = nombre
        if email:
            user.email = email
        if rol:
            user.rol = rol

        result = db.update_user(user)
        print("Usuario modificado:", result)

        flash('Usuario modificado correctamente', 'info')

    if rol:
        return redirect(url_for('main.user_list'))
    else:
        return redirect(url_for('main.profile'))


@main.route('/client_edit', methods=['POST'])
@login_required
def client_edit_post():
    id = request.form.get('id')
    email = request.form.get('email')
    nombre = request.form.get('nombre')
    sexo = request.form.get('sexo')
    patologia = request.form.get('patologia')
    fecha_nac = request.form.get('fecha_nac')

    user = db.get_user_by_id(id)

    today = date.today()

    if user.id:
        if nombre:
            user.nombre = nombre
        if email:
            user.email = email
        if sexo:
            user.sexo = sexo
        if fecha_nac:
            user.fecha_nac = fecha_nac
            fecha_nac = datetime.strptime(user.fecha_nac, '%Y-%m-%d')
            user.edad = today.year - fecha_nac.year - ((today.month, today.day) < (fecha_nac.month, fecha_nac.day))
        if patologia:
            user.patologia = patologia

        result = db.update_user(user)
        print("Cliente modificado:", result)

        flash('Cliente modificado correctamente', 'info')

    return redirect(url_for('main.client_list'))


@main.route('/user_remove/<string:id>')
@login_required
def user_remove(id):
    print("Eliminando usuario por id:", id)
    user = db.delete_user(id)
    flash("¡Usuario eliminado con éxito!", 'info')
    return redirect(url_for('main.user_list'))


@main.route('/user_change_password/<string:id>')
@login_required
def user_change_password(id):
    print("Recuperando usuario por id:", id)
    user = db.get_user_by_id(id)
    return render_template('user_change_password.html', user=user)


@main.route('/user_change_password', methods=['POST'])
@login_required
def user_change_password_post():
    id = request.form.get('id')
    password = request.form.get('password')
    password_repeat = request.form.get('password_repeat')

    if password != password_repeat:
        flash(f"Las contraseñas tienen que ser idénticas {password} {password_repeat}", "error")
        return redirect(url_for('main.user_change_password', id=id))

    user = db.get_user_by_id(id)

    if user.id:
        if password:
            user.password = generate_password_hash(password, method='sha256')

        result = db.update_user(user)
        print(result)

        flash('Contraseña cambiada correctamente')

    return redirect(url_for('main.user_list'))


@main.route('/client_remove/<string:id>')
@login_required
def client_remove(id):
    print("Eliminando cliente por id:", id)
    user = db.delete_user(id)
    flash("Cliente eliminado con éxito!", 'info')
    return redirect(url_for('main.client_list'))
