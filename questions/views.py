from django.shortcuts import render, redirect
from django.views import generic
from django.http import Http404

from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
import requests
from django.utils import timezone



from .forms import QuestionForm
from .models import Question

# Create your views here.
from . import models
from .forms import QuestionForm
# from braces.views import SelectRelatedMixin

from django.contrib.auth import get_user_model
User = get_user_model()

#views go here

class QuestionList(generic.ListView):
    # ^ took out SelectRelatedMixin, replace when ready
    model = models.Question


class CreateQuestion(generic.CreateView):
    model = models.Question
    form_class = QuestionForm
    # fields = ('question', 'answer')
    template_name = "questions/question_form_create.html"
    success_url = reverse_lazy('questions:all')
    # template name is NECESSARY FOR CREATE


class UserQuestions(generic.ListView):
    model = models.Question
    template_name = "questions/user_question_list.html"
    # completedTODO: CREATE user_question_list.html

    def get_queryset(self):
        try:
            self.question_user = User.objects.prefetch_related("questions").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.question_user.questions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_user"] = self.question_user
        return context










class QuestionDetail(generic.DetailView):
    model = models.Question



class QuestionUpdate(generic.UpdateView):
    model = models.Question
    form_class = QuestionForm
    template_name = "questions/question_form_update.html"
    #template name is NECESSARY FOR UPDATE instead of saving another



class QuestionDelete(generic.DeleteView):
    model = models.Question
    success_url = reverse_lazy('questions:all')

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Question Deleted")
        return super().delete(*args, **kwargs)









