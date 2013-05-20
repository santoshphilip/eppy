# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

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