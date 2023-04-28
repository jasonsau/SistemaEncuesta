from django.http import HttpResponse

from .Form.InputForm import InputForm
from .Form.SelectForm import SelectForm
from .Form.ITypeForm import ITypeForm
from .models import Polls, Questions, QuestionConfiguration, QuestionOptions
from django.core.serializers import serialize


def index(request):
    print(request)
    i_type_form: ITypeForm = SelectForm()

    options = [
        {
            'value': 'Pregunta 1',
            'name': 'pregunta1',
            'id': '2',

        },
        {
            'value': 'Pregunta 2',
            'name': 'pregunta2',
            'id': '3'
        },
    ]
    option_input = [
        {
            'value': 'Pregunta input',
            'name': 'preguntainput',
            'id': '4'
        }
    ]
    #string_html = i_type_form.return_html(options)
    i_type_form = InputForm()
    #string_html = string_html + i_type_form.return_html(option_input)
    questions = Questions.objects.filter(poll_question_id=1)
    questionConfiguration = []
    poll = Polls.objects.filter(id_poll=1)
    return HttpResponse(serialize('json', poll))
    string_test_from = "<h1>" + poll.name_poll + "</h1>"
    string_test_from = string_test_from + "<p>" + poll.description_poll + "</p>"
    string_test_from = string_test_from + "<p>" + poll.objetive_poll + "</p>"

    for question in questions:
        questionConfiguration = QuestionConfiguration.objects.filter(question_configuration_id=question.id_question).first()
        questionOptions = QuestionOptions.objects.filter(question_configuration_options_id=questionConfiguration.id_question_configuration)
        string_test_from = string_test_from + "<h2>" + question.title_question + "</h2>"
        i_type_form = get_type_form(questionConfiguration.type_question_configuration.name_type_question)
        string_test_from = string_test_from + i_type_form.return_html(questionOptions)

    return HttpResponse(string_test_from)


def get_type_form(type_form: str) -> ITypeForm:
    if type_form == 'input':
        return InputForm()
    elif type_form == 'select':
        return SelectForm()

def hello_word(request):
    return HttpResponse("Hello Word")