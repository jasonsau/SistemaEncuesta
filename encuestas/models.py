from django.db import models


class Polls(models.Model):
    id_poll = models.TextField(primary_key=True)
    name_poll = models.TextField(max_length=200)
    description_poll = models.TextField(max_length=500)
    objetive_poll = models.TextField(max_length=500)
    date_created_poll = models.DateTimeField(auto_created=True)
    date_updated_poll = models.DateTimeField(auto_now=True)
    active_poll = models.BooleanField(default=True)


class TypeQuestion(models.Model):
    id_type_question = models.TextField(primary_key=True)
    name_type_question = models.TextField(max_length=50)


class Questions(models.Model):
    id_question = models.TextField(primary_key=True)
    title_question = models.TextField(max_length=300)
    poll_question = models.ForeignKey(Polls, on_delete=models.CASCADE)


class QuestionConfiguration(models.Model):
    id_question_configuration = models.TextField(primary_key=True)
    question_configuration = models.OneToOneField(Questions, on_delete=models.CASCADE)
    label_question_configuration = models.TextField(max_length=50)
    type_question_configuration = models.ForeignKey(TypeQuestion, on_delete=models.CASCADE)


class QuestionOptions(models.Model):
    id_question_options = models.TextField(primary_key=True)
    name_question_options = models.TextField(max_length=100)
    value_question_options = models.TextField(max_length=50)
    label_question_options = models.TextField(max_length=50)
    question_configuration_options = models.ForeignKey(QuestionConfiguration, on_delete=models.CASCADE)
