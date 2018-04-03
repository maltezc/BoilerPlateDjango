from django.shortcuts import render, redirect
from django.views import generic
from django.http import Http404

from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
import requests
from django.utils import timezone

from taggit.models import Tag

from django.contrib.auth.decorators import login_required


from .forms import QuestionForm
from .models import Question, Comment

# Create your views here.
from . import models
from .forms import QuestionForm, CommentForm
# from braces.views import SelectRelatedMixin

from django.contrib.auth import get_user_model
User = get_user_model()

#views go here

class TagMixin(object):
    def get_context_data(self, kwargs):
        context = super(TagMixin, self).get_context_data(kwargs)
        context['tags'] = Tag.objects.all()
        return context


class QuestionList(generic.ListView):
    # ^ took out SelectRelatedMixin, replace when ready
    model = models.Question


class CreateQuestion(generic.CreateView):
    model = models.Question
    form_class = QuestionForm
    template_name = "questions/question_form_create.html"
    success_url = reverse_lazy('questions:all')
    # template name is NECESSARY FOR CREATE
    # fields = ('question', 'answer') <-- cant have fields and form_class in same view

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


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




def add_comment(request, pk, slug):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
            return redirect('questions:detail', pk=question.pk, slug=question.slug)
    else:
        form = CommentForm()
    return render(request, 'questions/add_comment.html', {'form': form})


# @login_required
# def comment_approve(request, pk, slug):
#     comment = get_object_or_404(Comment, pk=pk, slug=slug)
#     comment.approve()
#     return redirect('question:detail', pk=comment.question.pk, slug=comment.question.slug)
#
#
# @login_required
# def comment_remove(request, pk, slug):
#     comment = get_object_or_404(Comment, pk=pk, slug=slug)
#     comment.delete()
#     return redirect('question:detail', pk=comment.question.pk, slug=comment.question.slug)
#

