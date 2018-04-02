from django import forms
from django.contrib.auth.models import User
# from questions import models
from .models import Question, Comment

class QuestionForm(forms.ModelForm):
    # your_name = forms.CharField(label='Your name', max_length=100)
    class Meta:
        fields = ("question", 'answer', 'tags')
        model = Question


class CommentForm(forms.ModelForm):

    class Meta:
        fields = ('author', 'text')
        model = Comment








