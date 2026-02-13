from django.db import models
from datetime import datetime
from asyncio.windows_events import NULL
from operator import mod

# Create your models here.

class QuestionModel(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.TextField(verbose_name='Question', blank=False, null=False)
    answer = models.TextField(verbose_name='Answers', null=True, blank=True)
    subject = models.CharField(verbose_name='Subject', max_length=100, blank=False, null=False)
    datetime_created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'question_answer'


class SubjectModel(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject = models.CharField(verbose_name='Subject', max_length=100, blank=False, null=False)
    subject_image = models.FileField(verbose_name='Photo', upload_to='media', blank=False)
    datetime_created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'subject_details'
