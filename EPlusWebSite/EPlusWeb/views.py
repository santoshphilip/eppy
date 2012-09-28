# Create your views here.
"""build the topology of the plant loop, and generate an idf for it."""
import sys
sys.path.append('../EPlusInputcode')
sys.path.append('../diagrams')
from EPlusCode.EPlusInterfaceFunctions import readidf

from EPlusCode.EPlusInterfaceFunctions import parse_idd
from EPlusCode.EPlusInterfaceFunctions import eplusdata
from EPlusCode.EPlusInterfaceFunctions import mylib3


import eplus_functions
import idd_fields

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

iddfile = "../iddfiles/Energy+V6_0.idd"
block,commlst,commdct=parse_idd.extractidddata(iddfile)
theidd=eplusdata.idd(block,2)

fname = "../idffiles/a.idf"
# fname = "../idffiles/HVACTemplate-5ZoneFanCoil.idf"
data, commdct = readidf.readdatacommdct(fname, iddfile=theidd,
                            commdct=commdct)


idd = eplus_functions.Idd(commdct, commlst, theidd, block)
idfw = eplus_functions.IdfWrapper(data, idd)





def idfview(request):
    txt = `idfw`
    txt = txt.replace(mylib3.dossep, "<br>")
    return HttpResponse(txt)
    
def keys(request):
    dt = idfw.idf.dt
    dtls = idfw.idf.dtls
    kys = dt.keys()
    kys = [k for k in kys if len(dt[k]) > 0]
    nkys = [k for k in dtls if k in kys]
    nkys = ["[%s] %s" % (len(dt[k]), k) for k in nkys]
    txt = '<br>'.join(nkys)
    return HttpResponse(txt)

def tmpl(request):
    # latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('viewtemplates/index.html')
    c = Context({
        'latest_poll_list': [1,2,3],
    })
    return HttpResponse(t.render(c))
    
def allkeys(request):
    dt = idfw.idf.dt
    dtls = idfw.idf.dtls
    kys = dt.keys()
    kys = [k for k in kys if len(dt[k]) > 0]
    nkys = [(i, k) for i, k in enumerate(dtls) if k in kys]
    thekeys = [(i, len(dt[k]), k) for i, k in nkys]
    dct = {'keylist': thekeys}
    return render_to_response('viewtemplates/allkeys.html', dct)
    
def akey(request, keyid):
    keyid = int(keyid)
    dt = idfw.idf.dt
    idf = idfw.idf
    dtls = idfw.idf.dtls
    thekey = dtls[keyid]
    commdct = idfw.idd.commdct
    # try:
    #     fieldindex = eplus_functions.getfieldindex(idf, commdct, thekey,
    #                                             idd_fields.ObjectName.name)
    # except eplus_functions.NoSuchFieldError, e:
    #     fieldindex = eplus_functions.getfieldindex(idf, commdct, thekey,
    #                                     idd_fields.ObjectName.variablename)
    fieldindex = 1 # above code does not work since some of them have no names
    objnames = [(i, obj[fieldindex]) for i, obj in enumerate(dt[thekey])]
    fieldindices = [1, 2]
    try:
        objnames = [(i, [obj[j] for j in fieldindices]) for i, obj in enumerate(dt[thekey])]
    except IndexError, e:
        fieldindices = [1, ]
        objnames = [(i, [obj[j] for j in fieldindices]) for i, obj in enumerate(dt[thekey])]
    # objnames = [(i, [obj for obj in objs]) for i, objs in enumerate(dt[thekey])]
    dct = {'thekey': thekey, 'theobjects': objnames, 'keyid':keyid}
    return render_to_response('viewtemplates/akey.html', dct)

def anobject(request, keyid, objid):
    objid = int(objid)
    keyid = int(keyid)
    dt = idfw.idf.dt
    idf = idfw.idf
    dtls = idfw.idf.dtls
    thekey = dtls[keyid]
    commdct = idfw.idd.commdct
    fieldvalues = dt[dtls[keyid]][objid]
    fieldnames = eplus_functions.getobjfieldnames(idf, commdct, thekey)
    index_field_name = enumerate(zip(fieldvalues, fieldnames)[1:])
    fields = [(i + 1, f, n) for i, (f, n) in index_field_name]
    dct = {'thekey': thekey, 'fields': fields, 'keyid': keyid, 'objid':objid}
    return render_to_response('viewtemplates/anobject.html', dct)

def editfield(request, keyid, objid, fieldid):
    objid = int(objid)
    keyid = int(keyid)
    fieldid = int(fieldid)
    dt = idfw.idf.dt
    idf = idfw.idf
    dtls = idfw.idf.dtls
    thekey = dtls[keyid]
    avar = keyid
    fieldnameindex = 1 # this is not always true
    objname = dt[dtls[keyid]][objid][fieldnameindex]
    fieldname = eplus_functions.getobjfieldnames(idf, commdct, 
                                                    thekey)[fieldid]
    fieldvalue = dt[dtls[keyid]][objid][fieldid] 
    cdct = commdct[keyid][fieldid]
    cdct = [(key, value) for key, value in cdct.items()]
    funcs = [eplus_functions.getobjlistOfField, eplus_functions.getchoiceOFField]
    alist = []
    for func in funcs:
        if not alist:
            alist = func(idfw, thekey, objid, fieldid)
    dct = {'avar':value, 'thekey': thekey, 'objname':objname, 
        'fieldname':fieldname, 'value':fieldvalue, 'cdct':cdct,
        'keyid':keyid, 'objid':objid, 'fieldid':fieldid, 'objlist':alist}
    return render_to_response('viewtemplates/editfield.html', dct,
                    context_instance=RequestContext(request))
    
def updatefield(request, keyid, objid, fieldid):
    """update the field data with data coming from the form"""
    print request.POST.keys()
    dt = idfw.idf.dt
    dtls = idfw.idf.dtls
    keyid, objid, fieldid = [int(i) for i in [keyid, objid, fieldid]]
    s = str(request.POST['fieldvalue'])
    newname = s
    key = dtls[keyid]
    oldname = dt[key][objid][fieldid]
    dt[key][objid][fieldid] = s
    eplus_functions.newname2references(idfw, key, fieldid, oldname, newname)
    return HttpResponseRedirect("../../../../anobject/%s/%s/" % (keyid, objid))
    

def home(request):
    """home page"""
    dct = {}
    return render_to_response('viewtemplates/home.html', dct)
