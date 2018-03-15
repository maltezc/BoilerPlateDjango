from django.db import models
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
import misaka # http://misaka.61924.nl/
#Misaka is a CFFI-based binding for Hoedown, a fast markdown processing library written in C.
# It features a fast HTML renderer and functionality to make custom renderers (e.g. man pages or LaTeX).
from django.utils import timezone


User = get_user_model()

class Question(models.Model):
    user = models.ForeignKey(User, related_name="question", default='')
    question = models.TextField(unique=False, default='')
    question_html = models.TextField(default='')
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.question
        # ^ to display an object in the Django admin site and
        # as the value inserted into a template when it displays an object.

    def save(self, *args, **kwargs):
        self.question_html = misaka.html(self.question)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(
            "questions:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

class Answer(models.Model):
    user = models.ForeignKey(User, related_name="answer", default='')
    answer = models.TextField(unique=False, default='')
    answer_html = models.TextField(default='')
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.answer

    def save(self, *args, **kwargs):
        self.answer_html = misaka.html(self.answer)
        super().save(*args, **kwargs)

