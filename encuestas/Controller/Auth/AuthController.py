import json
import bcrypt
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from ...models import Persons, Users
from django.contrib.auth import login as auth_login, logout as auth_logout


def login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    return render(request, 'auth/login.html')


def login_post(request):
    data_json = json.loads(request.body)
    person = Persons.objects.filter(email_person=data_json['email']).first()
    if person is None:
        return HttpResponse(json.dumps({"status": "error", "message": "Creedenciales incorrectas"}))

    user = Users.objects.filter(person_user=person.id_person).first()
    if user is None:
        return HttpResponse(json.dumps({"status": "error", "message": "Creedenciales incorrectas"}))

    if not user.active_person:
        return HttpResponse(json.dumps({"status": "error", "message": "Su usuario ha sido bloqueado"}))

    if not bcrypt.checkpw(data_json['password'].encode('utf-8'), user.password_user.encode('utf-8')):
        user.fails_login_user += 1
        if user.fails_login_user >= 3:
            user.active_person = False
            user.fails_login_user = 0
        user.save()
        return HttpResponse(json.dumps({"status": "error", "message": "Creedenciales incorrectas"}))

    auth_login(request, user)

    return HttpResponse(json.dumps({"status": "success", "message": "Bienvenido"}))


def register_user(request):
    cursor = connection.cursor()
    data_json = json.loads(request.body)
    errors = validate_data(data_json)
    password = bcrypt.hashpw(
        data_json['user']['password_user'].encode('utf-8'),
        bcrypt.gensalt()
    )
    print(data_json)
    if len(errors['errors']) > 0:
        return HttpResponse(json.dumps(errors), content_type="application/json")
    try:
        cursor.execute('call procedure_register_person(%s, %s)', [json.dumps(data_json), password])
        cursor.close()
    except Exception as e:
        print("Hay un error")
        print(e)
        cursor.close()
        return HttpResponse(json.dumps({"status": "error", "message": "Error al registrar usuario"}))
    return HttpResponse(json.dumps({"status": "success", "message": "Usuario registrado correctamente"}))


def logout(request):
    auth_logout(request)
    return redirect('/login')


def validate_data(data_json: dict) -> dict:
    error: dict = {
        'status': 'error',
        'errors': [],
        'message': 'Error al validar datos'
    }
    error_name_person = []
    error_email_person = []
    error_genre_person = []
    error_password_person = []
    error_confirm_password = []
    error_birth_date_person = []

    if data_json['person']['name_person'] == '':
        error_name_person.append('El nombre es requerido')
    if len(data_json['person']['name_person']) > 100:
        error_name_person.append('El nombre no puede tener mas de 100 caracteres')

    if data_json['person']['email_person'] == '':
        error_email_person.append('El correo es requerido')
    if len(data_json['person']['email_person']) > 100:
        error_email_person.append('El correo no puede tener mas de 100 caracteres')

    if data_json['person']['genre_person'] == '':
        error_genre_person.append('El genero es requerido')

    if not data_json['person']['genre_person'] == 'M' or data_json['person']['genre_person'] == 'F':
        error_genre_person.append('El genero no es valido, debe ser Masculino o Fememino')

    if data_json['user']['password_user'] == '':
        error_password_person.append('La contraseña es requerida')
    if len(data_json['user']['password_user']) > 100:
        error_password_person.append('La contraseña no puede tener mas de 100 caracteres')

    if data_json['user']['confirm_password'] == '':
        error_confirm_password.append('La confirmacion de contraseña es requerida')

    if len(data_json['user']['confirm_password']) > 100:
        error_confirm_password.append('La contraseña no puede tener mas de 100 caracteres')

    if not data_json['user']['password_user'] == data_json['user']['confirm_password']:
        error_confirm_password.append('Las contraseñas no coinciden')

    if data_json['person']['birth_date_person'] == '':
        error_birth_date_person.append('La fecha de nacimiento es requerida')

    error['errors'].append({'name_person': error_name_person, 'field': 'name_person'})
    error['errors'].append({'email_person': error_email_person, 'field': 'email_person'})
    error['errors'].append({'genre_person': error_genre_person, 'field': 'genre_person'})
    error['errors'].append({'register_password': error_password_person, 'field': 'register_password'})
    error['errors'].append({'confirm_password': error_confirm_password, 'field': 'confirm_password'})
    error['errors'].append({'birth_date_person': error_birth_date_person, 'field': 'birth_date_person'})
    count_error: int = 0
    for e in error['errors']:
        if len(e[e['field']]) > 0:
            count_error += 1
    if count_error > 0:
        return error

    return {'status': 'error', 'errors': []}


def check_permissions(request):
    result_bool: bool = True
    path_name = request.path[1:]
    with connection.cursor() as cursor:
        cursor.callproc('procedure_check_permissions', [request.user.id_user, path_name, result_bool])
        result_bool = cursor.fetchone()[0]
    return result_bool


