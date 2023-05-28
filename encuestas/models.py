from django.db import models


class Persons(models.Model):
    id_person = models.AutoField(primary_key=True)
    name_person = models.TextField(max_length=50)
    birth_date_person = models.DateField()
    img_person = models.TextField(max_length=250, null=True)
    email_person = models.TextField(max_length=50)
    genre_person = models.TextField(max_length=1)
    active_person = models.BooleanField(default=True)


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    username_user = models.TextField(max_length=50)
    password_user = models.TextField(max_length=255)
    person_user = models.ForeignKey(Persons, on_delete=models.CASCADE)
    token_user = models.TextField(max_length=255, null=True)
    fails_login_user = models.IntegerField(default=0)
    active_person = models.BooleanField(default=True)


class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    name_rol = models.TextField(max_length=50)
    description_rol = models.TextField(max_length=250)
    active_rol = models.BooleanField(default=True)


class UserRoles(models.Model):
    id_user_rol = models.AutoField(primary_key=True)
    user_user_rol = models.ForeignKey(Users, on_delete=models.CASCADE)
    rol_user_rol = models.ForeignKey(Roles, on_delete=models.CASCADE)


class Permissions(models.Model):
    id_permission = models.AutoField(primary_key=True)
    name_permission = models.TextField(max_length=50)
    description_permission = models.TextField(max_length=250)
    active_permission = models.BooleanField(default=True)


class RolPermissions(models.Model):
    id_rol_permission = models.AutoField(primary_key=True)
    rol_rol_permission = models.ForeignKey(Roles, on_delete=models.CASCADE)
    permission_rol_permission = models.ForeignKey(Permissions, on_delete=models.CASCADE)


class HistoryPassword(models.Model):
    id_history_password = models.AutoField(primary_key=True)
    user_history_password = models.ForeignKey(Users, on_delete=models.CASCADE)
    password_history_password = models.TextField(max_length=255)
    date_created_history_password = models.DateTimeField(auto_created=True)


class Polls(models.Model):
    id_poll = models.AutoField(primary_key=True)
    title_poll = models.TextField(max_length=200)
    object_poll = models.TextField(max_length=500)
    date_created_poll = models.DateTimeField(auto_created=True)
    description_poll = models.TextField(max_length=500)
    instructions_poll = models.TextField(max_length=500)
    date_start_poll = models.DateTimeField()
    date_end_poll = models.DateTimeField()
    token_poll = models.TextField(max_length=255, unique=True)
    limit_sample_poll = models.IntegerField(default=10000)
    user_poll = models.ForeignKey(Persons, on_delete=models.CASCADE)


class TypeQuestion(models.Model):
    id_type_question = models.AutoField(primary_key=True)
    name_type_question = models.TextField(max_length=50)
    description_type_question = models.TextField(max_length=250)


class Questions(models.Model):
    id_question = models.AutoField(primary_key=True)
    title_question = models.TextField(max_length=300)
    poll_question = models.ForeignKey(Polls, on_delete=models.CASCADE)
    type_question_question = models.ForeignKey(TypeQuestion, on_delete=models.CASCADE)


class OptionsQuestion(models.Model):
    id_option_question = models.AutoField(primary_key=True)
    question_option_question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    title_option_question = models.TextField(max_length=250)
    name_option_question = models.TextField(max_length=50)
    description_option_question = models.TextField(max_length=250, null=True)
    value_option_question = models.TextField(default="")
    id_option = models.TextField(max_length=100, null=True)
    order_option_question = models.IntegerField(default=0, null=True)


class Answers(models.Model):
    id_answer = models.AutoField(primary_key=True)
    poll_answer = models.ForeignKey(Polls, on_delete=models.CASCADE)
    date_created_answer = models.DateTimeField(auto_created=True)
    token_answer = models.TextField(max_length=255)
    birth_date_answer = models.DateField(null=True)
    genre_answer = models.TextField(max_length=1, null=True)
    email_answer = models.TextField(max_length=50, null=True)
    name_answer = models.TextField(max_length=50, null=True)


class AnswersQuestions(models.Model):
    id_answer_question = models.AutoField(primary_key=True)
    answer_answer_question = models.ForeignKey(Answers, on_delete=models.CASCADE)
    option_answer_question = models.ForeignKey(OptionsQuestion, on_delete=models.CASCADE, null=True)
    value_answer_question = models.IntegerField(default=0, null=True)
    text_answer_question = models.TextField(max_length=500, null=True)
    date_created_answer_question = models.DateTimeField(auto_created=True)
    token_answer_question = models.TextField(max_length=255, null=True)
