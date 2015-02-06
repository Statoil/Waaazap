from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.


def hello(request):
    helloView = loader.get_template('webfront/hello.html')
    context = RequestContext(request)
    return HttpResponse(helloView.render(context))