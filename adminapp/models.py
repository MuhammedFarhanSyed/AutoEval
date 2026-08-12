from django.db import models
from datetime import datetime

# ==============================================================================
# ADMIN APP DATABASE MODELS
# ==============================================================================

class QuestionModel(models.Model):
    """
    Model representing an exam question and its reference model answer created by the admin.
    
    Fields:
        question_id: Primary Key (auto-incrementing integer).
        question: Full text of the exam question.
        answer: Reference model answer uploaded by faculty for automated evaluation.
        subject: Subject name associated with this question.
        datetime_created: Creation timestamp.
    """
    question_id = models.AutoField(primary_key=True)
    question = models.TextField(verbose_name='Question', blank=False, null=False)
    answer = models.TextField(verbose_name='Answers', null=True, blank=True)
    subject = models.CharField(verbose_name='Subject', max_length=100, blank=False, null=False)
    datetime_created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'question_answer'  # Custom database table name in MySQL


class SubjectModel(models.Model):
    """
    Model representing an academic subject/course created by the admin.
    
    Fields:
        subject_id: Primary Key (auto-incrementing integer).
        subject: Name of the subject (e.g., 'Python', 'Java').
        subject_image: Thumbnail image for the subject card uploaded to media folder.
        datetime_created: Creation timestamp.
    """
    subject_id = models.AutoField(primary_key=True)
    subject = models.CharField(verbose_name='Subject', max_length=100, blank=False, null=False)
    subject_image = models.FileField(verbose_name='Photo', upload_to='media', blank=False)
    datetime_created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'subject_details'  # Custom database table name in MySQL

