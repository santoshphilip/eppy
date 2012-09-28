"""This is where I try out stuff"""
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
import pickle

def learn(request):
    """just learn"""
    return HttpResponse("just learn")


def atemplate(request):
    """just a template"""
    dct = {}
    return render_to_response('learntemplates/atemplate.html', dct)
    
def anedit(request):
    """just a template"""
    dct = {}
    return render_to_response('learntemplates/anedit.html', dct,
        context_instance=RequestContext(request))
    
def formdata(request):
    """show the post data from the form"""
    keyvals = request.POST.items()
    print dict(keyvals)
    print request.POST['text']
    s = str(request.POST['text'])
    return HttpResponseRedirect("../edited")
    # return HttpResponse(s)    
    # return render_to_response('polls/detail.html', {'poll': p})
    
def edited(request):
    """docstring for edited"""
    return HttpResponse("editing done")