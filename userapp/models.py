from django.db import models
from datetime import datetime
from django.utils import timezone
from adminapp.models import *

# ==============================================================================
# USER APP DATABASE MODELS
# ==============================================================================

class UserdetailsModel(models.Model):
    """
    Model storing student/user registration details and account statuses.
    
    Fields:
        user_id: Primary Key (auto-incrementing integer).
        user_name: Full name of student.
        user_email: Email address used for login authentication.
        user_contact: Phone/contact number.
        user_password: User password.
        student_id: Student identification number / registration ID.
        user_photo: Uploaded profile picture stored in media directory.
        datetime_created: Account creation date and time.
        user_status: Approval status ('pending', 'accepted', 'declined', 'blocked').
    """
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(verbose_name='Name', max_length=50, blank=False, null=False)
    user_email = models.CharField(verbose_name='Email', max_length=100, null=True, blank=True)
    user_contact = models.BigIntegerField(verbose_name='contact', blank=False, null=False)
    user_password = models.CharField(verbose_name='Password', max_length=100, blank=False, null=False)
    student_id = models.CharField(verbose_name='Student ID', max_length=100, blank=False, null=False)
    user_photo = models.FileField(verbose_name='Photo', upload_to='media', blank=False)
    datetime_created = models.DateTimeField(default=datetime.now)
    user_status = models.CharField(default='pending', max_length=50, null=True)

    class Meta:
        db_table = 'user_details'  # Custom database table name in MySQL


class AnswerModel(models.Model):
    """
    Model storing evaluated exam submissions submitted by students.
    
    Fields:
        answer_id: Primary Key.
        answer_subject: Subject name of the exam.
        answer: Serialized dictionary string storing questions, student answers, and individual marks.
        user_id: Foreign key linking to the student (UserdetailsModel).
        score: Total calculated score out of 100.
        grade: Final evaluated letter grade ('A', 'B', 'C', 'F').
        datetime_answered: Timestamp of exam submission.
    """
    answer_id = models.AutoField(primary_key=True)
    answer_subject = models.CharField(verbose_name='Subject', max_length=50, blank=False, null=False)
    answer = models.TextField(verbose_name='Answer', null=True, blank=True)
    user_id = models.ForeignKey(UserdetailsModel, on_delete=models.CASCADE, related_name='Examinee', null=True)
    score = models.IntegerField(blank=False, null=True)
    grade = models.CharField(verbose_name='Grade', max_length=100, blank=False, null=True)
    datetime_answered = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_answers'  # Custom database table name in MySQL


class TempModel(models.Model):
    """
    Temporary helper model used to unpack and display itemized question-wise results.
    
    Fields:
        answer_id: Primary Key.
        subject: Subject name.
        question: Question text.
        answer: Student's answer.
        score: Score obtained for this specific question.
    """
    answer_id = models.AutoField(primary_key=True)
    subject = models.CharField(verbose_name='Subject', max_length=50, blank=False, null=False)
    question = models.TextField(verbose_name='Question', null=True, blank=True)
    answer = models.TextField(verbose_name='Answer', null=True, blank=True)
    score = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        db_table = 'temp_model'  # Custom database table name in MySQL
