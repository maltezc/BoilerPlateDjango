from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

#here you create basic pages


#home page
class HomePage(TemplateView):
    template_name = "index.html"

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated():
    #         return HttpResponseRedirect(reverse("test"))
    #     return super().get(request, *args, **kwargs)


class TestPage(TemplateView):
    template_name = 'test.html'