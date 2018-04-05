from django.db import models
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save
from django.utils.text import slugify

import misaka # http://misaka.61924.nl/
#Misaka is a CFFI-based binding for Hoedown, a fast markdown processing library written in C.
# It features a fast HTML renderer and functionality to make custom renderers (e.g. man pages or LaTeX).
from django.utils import timezone

User = get_user_model()

class Question(models.Model):
    class Meta:
        ordering = ['-date_updated']
    user = models.ForeignKey(User, related_name="questions")
    # completedTODO: get user working^
    question = models.TextField(blank=False, null=False) # unique=True,
    question_html = models.TextField(blank=False, null=False)
    answer = models.TextField(blank=False, null=False)
    answer_html = models.TextField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(unique=True, default='')
    tags = TaggableManager()


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
                "slug": self.slug,
                "pk": self.pk,
                "username": self.user.username,

            }
        )

def create_slug(instance, new_slug=None):
    slug = slugify(instance.question)
    if new_slug is not None:
        slug = new_slug
    qs = Question.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_question_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


    # slug = slugify(instance.question)
    # exists = Question.objects.filter(slug=slug).exists()
    # if exists:
    #     slug = "%s-%s" %(slug, instance.id)
    # instance.slug = slug

pre_save.connect(pre_save_question_receiver, sender=Question)

class Comment(models.Model):
    question = models.ForeignKey(Question, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField(null=False, blank=False, default='')
    date_created = models.DateTimeField(default=timezone.now)
    # approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text


    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    # def approved_comments(self):
#     return self.comments.filter(approved_comment=True)

# TODO: create point system
# TODO: create up vote system
