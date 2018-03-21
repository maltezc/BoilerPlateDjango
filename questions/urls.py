from django.conf.urls import url
from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^questionslist/$', views.QuestionList.as_view(), name='all'),
    url(r'new/$', views.CreateQuestion.as_view(), name='create'),
    # url(r'by/(?P<username>[-\w]+)/$', views.UserQuestions.as_view(), name="for_user"),
    url(r'questionupdate/(?P<pk>\d+)/$', views.QuestionUpdate.as_view(), name='update'),
    # url(r'by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.QuestionDetail.as_view(), name="single"),
    url(r'questiondetail/(?P<pk>\d+)/$', views.QuestionDetail.as_view(), name='detail'),
    url(r'delete/(?P<pk>\d+)/$', views.QuestionDelete.as_view(), name='delete'),

]