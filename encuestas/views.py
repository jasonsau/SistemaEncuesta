from django.http import HttpResponse


def index(request):
    return "Hello Wordl"


def hello_word(request):
    return HttpResponse("Hello Word")