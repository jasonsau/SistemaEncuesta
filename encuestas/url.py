from django.urls import path
from .Controller.PollController import create_poll, store_poll, get_poll, get_data_poll

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hello-word", views.hello_word, name="hello_word"),
    path("create-poll", create_poll, name="create_poll"),
    path("save-poll", store_poll, name="save_poll"),
    path("get-poll/<str:token_poll>", get_poll, name="get_poll"),
    path("get-data-poll/<str:token_poll>", get_data_poll, name="get_data_poll"),


]
