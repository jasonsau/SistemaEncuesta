from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def hello_word(request):
    return HttpResponse("Hello Word")