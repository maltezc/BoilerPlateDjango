from django.db import models
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


import misaka # http://misaka.61924.nl/
#Misaka is a CFFI-based binding for Hoedown, a fast markdown processing library written in C.
# It features a fast HTML renderer and functionality to make custom renderers (e.g. man pages or LaTeX).
from django.utils import timezone

User = get_user_model()

class Question(models.Model):
    class Meta:
        ordering = ['-date_updated']
    # user = models.ForeignKey(User, related_name="question", default='')
    # TODO: get user working^
    question = models.TextField(blank=False, null=False) # unique=True,
    question_html = models.TextField(blank=False, null=False)
    answer = models.TextField(blank=False, null=False)
    answer_html = models.TextField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.question
        # ^ to display an object in the Django admin site and
        # as the value inserted into a template when it displays an object.

    def save(self, *args, **kwargs):
        self.question_html = misaka.html(self.question)
        self.answer_html = misaka.html(self.answer)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "questions:detail",
            kwargs={
                # "username": self.user.username,
                "pk": self.pk
            }
        )
