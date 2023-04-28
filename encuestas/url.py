from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hello-word", views.hello_word, name="hello_word")
]
