from django.urls import path
from .Controller.PollController import create_poll, store_poll, get_poll, get_data_poll, response_poll, get_type_question
from .Controller.HomeController import home

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hello-word", views.hello_word, name="hello_word"),
    path("create-poll", create_poll, name="create_poll"),
    path("save-poll", store_poll, name="save_poll"),
    path("get-poll/<str:token_poll>", get_poll, name="get_poll"),
    path("get-type-questions", get_type_question, name="get_type_question"),

    path("response-poll/<str:token_poll>", response_poll, name="response_poll"),

    path("get-data-poll/<str:token_poll>", get_data_poll, name="get_data_poll"),
    path("home", home, name="home")

]
