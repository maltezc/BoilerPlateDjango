from django import forms
from questions import models


class QuestionForm(forms.ModelForm):
    # your_name = forms.CharField(label='Your name', max_length=100)
    class Meta:
        fields = ("question", 'answer')
        model = models.Question






