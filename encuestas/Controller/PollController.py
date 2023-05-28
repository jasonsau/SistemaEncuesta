import datetime
import random
import json

from django.http import HttpResponse
from ..models import Questions, Polls, OptionsQuestion, TypeQuestion, Persons
from django.shortcuts import render


def create_poll(request):
    return render(request, 'poll/create_poll.html')


def store_poll(request):
    if request.method == 'GET' or request.method == 'PUT' or request.method == 'DELETE':
        return HttpResponse("Method not allowed")

    data_json: dict = json.loads(request.body)

    error = validate_data(data_json)

    if len(error['errors']) > 0:
        return HttpResponse(json.dumps(error), content_type="application/json")



    user = Persons.objects.filter(id_person=1).first()
    poll = Polls()
    poll.description_poll = ''
    poll.title_poll = data_json['general']['name_poll']
    poll.instructions_poll = data_json['general']['instructions_poll']
    poll.object_poll = data_json['general']['objective_poll']
    poll.date_end_poll = data_json['general']['date_end_poll']
    poll.date_start_poll = data_json['general']['date_start_poll']
    poll.token_poll = generate_token_random(data_json['general']['name_poll'])
    poll.date_created_poll = datetime.datetime.now()
    poll.limit_sample_poll = data_json['general']['limit_sample_poll']
    poll.user_poll = user
    poll.save()

    for question in data_json['questions']:
        type = TypeQuestion.objects.filter(id_type_question=question['type_question']).first()
        question_temp = Questions()
        question_temp.title_question = question['title_question']
        question_temp.type_question_question = type
        question_temp.poll_question = poll
        question_temp.save()

        for option in question['options']:
            option_temp = OptionsQuestion()
            option_temp.id_option = option['id_question']
            option_temp.name_option_question = option['name_option']
            option_temp.value_option_question = option['value_option']
            option_temp.title_option_question = option['title_option']
            option_temp.description_option_question = ''
            option_temp.question_option_question = question_temp
            option_temp.save()

    return HttpResponse(json.dumps({
        'status': 'ok',
    }), content_type='application/json')


def get_poll(request, token_poll: str):
    poll = Polls.objects.filter(token_poll=token_poll).first()
    if poll is None:
        return HttpResponse("La encuesta no existe")

    if str(poll.date_start_poll) > str(datetime.datetime.now()):
        return HttpResponse("La encuesta aun no inicia")

    if str(poll.date_end_poll) < str(datetime.datetime.now()):
        return HttpResponse("La encuesta ya finalizo")

    return render(request, 'poll/get_poll.html')


def get_data_poll(request, token_poll: str):
    if request.method == 'POST':
        return HttpResponse("Method not allowed")

    poll = Polls.objects.filter(token_poll=token_poll).first()
    data_poll = {'general': {
        'name_poll': poll.title_poll,
        'instructions_poll': poll.instructions_poll,
        'objective_poll': poll.object_poll,
    }, 'questions': []}

    questions = Questions.objects.filter(poll_question=poll)

    for question in questions:
        question_temp = {
            'title_question': question.title_question,
            'type_question': question.type_question_question.id_type_question,
            'options': []
        }
        options = OptionsQuestion.objects.filter(question_option_question=question)

        for option in options:
            option_temp = {
                'id_question': option.id_option,
                'name_option': option.name_option_question,
                'value_option': option.value_option_question,
                'title_option': option.title_option_question,
                'description_option': '',
            }
            question_temp['options'].append(option_temp)

        data_poll['questions'].append(question_temp)

    return HttpResponse(json.dumps(data_poll), content_type='application/json')


def get_template_option_unique(request):
    return render(request, 'poll/option_unique.html')


def generate_token_random(title_question: str) -> str:
    array_title_question = title_question.split(' ')
    token = ''
    for word in array_title_question:
        token += word[0:2]
    return token + str(random.randint(1, 1000000))


def validate_data(data_json: dict) -> dict:
    error: dict = {
        'status': 'error',
        'errors': []
    }
    error_name_pool = []
    error_objective_pool = []
    error_date_start_pool = []
    error_date_end_pool = []
    error_limit_sample_pool = []
    error_instructions_pool = []
    error_questions = []

    if data_json['general']['name_poll'] == '':
        error_name_pool.append('El nombre de la encuesta es obligatorio')

    if len(data_json['general']['name_poll']) > 100:
        error_name_pool.append('El nombre de la encuesta no puede tener mas de 100 caracteres')

    if len(data_json['general']['name_poll']) < 4:
        error_name_pool.append('El nombre de la encuesta no puede tener menos de 4 caracteres')

    if data_json['general']['objective_poll'] == '':
        error_objective_pool.append('El objetivo de la encuesta es obligatorio')

    if len(data_json['general']['objective_poll']) > 500:
        error_objective_pool.append('El objetivo de la encuesta no puede tener mas de 500 caracteres')

    if len(data_json['general']['objective_poll']) < 4:
        error_objective_pool.append('El objetivo de la encuesta no puede tener menos de 4 caracteres')

    if data_json['general']['date_start_poll'] == '':
        error_date_start_pool.append('La fecha de inicio es obligatoria')

    if data_json['general']['date_end_poll'] == '':
        error_date_end_pool.append('La fecha de finalizacion es obligatoria')

    if data_json['general']['date_start_poll'] > data_json['general']['date_end_poll']:
        error_date_start_pool.append('La fecha de inicio no puede ser mayor a la fecha de finalizacion')

    print("*********************************")
    print(data_json['general']['date_start_poll'])
    print(str(datetime.date.today()))
    if data_json['general']['date_start_poll'] < str(datetime.date.today()):
        error_date_start_pool.append('La fecha de inicio no puede ser menor a la fecha actual')

    if data_json['general']['limit_sample_poll'] == '':
        error_limit_sample_pool.append('El limite de muestra es obligatorio')

    if data_json['general']['limit_sample_poll'] < 1:
        error_limit_sample_pool.append('El limite de muestra no puede ser menor a 1')

    if data_json['general']['instructions_poll'] == '':
        error_instructions_pool.append('Las instrucciones de la encuesta son obligatorias')

    if len(data_json['general']['instructions_poll']) > 500:
        error_instructions_pool.append('Las instrucciones de la encuesta no pueden tener mas de 500 caracteres')

    if len(data_json['general']['instructions_poll']) < 4:
        error_instructions_pool.append('Las instrucciones de la encuesta no pueden tener menos de 4 caracteres')

    if len(data_json['questions']) == 0:
        error_questions.append('Debe agregar al menos una pregunta')

    error['errors'].append({'objetive_poll': error_objective_pool, 'field': 'objetive_poll'})
    error['errors'].append({'name_poll': error_name_pool, 'field': 'name_poll'})
    error['errors'].append({'date_start_poll': error_date_start_pool, 'field': 'date_start_poll'})
    error['errors'].append({'date_end_poll': error_date_end_pool, 'field': 'date_end_poll'})
    error['errors'].append({'limit_sample_poll': error_limit_sample_pool, 'field': 'limit_sample_poll'})
    error['errors'].append({'instructions_poll': error_instructions_pool, 'field': 'instructions_poll'})
    error['errors'].append({'questions': error_questions, 'field': 'questions'})
    count_error: int = 0;
    for e in error['errors']:
        if len(e[e['field']]) > 0:
            count_error += 1

    if count_error > 0:
        print("Entra a los errores")
        print(error)
        return error

    return {'status': 'error', 'errors': []}
