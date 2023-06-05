from django.shortcuts import render
from ..models import Polls
from django.db import connection
from django.contrib.auth.decorators import login_required
from ..Controller.Auth.AuthController import check_permissions


@login_required(login_url='/login')
def home(request):
    user = request.user
    if not check_permissions(request):
        return render(request, 'errors/403.html')

    polls = Polls.objects.filter(user_poll=user.person_user).all()
    return render(request, 'home/index.html', {'user': user, 'polls': polls})

