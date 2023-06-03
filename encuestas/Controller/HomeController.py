from django.shortcuts import render
from ..models import Polls, Persons


def home(request):
    user = Persons.objects.filter(id_person=1).first()
    polls = Polls.objects.filter(user_poll=user).all()
    return render(request, 'home/index.html', {'user': user, 'polls': polls})
