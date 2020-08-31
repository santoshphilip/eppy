# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""make plant loop snippets"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy

import eppy.bunch_subclass as bunch_subclass
from eppy.modeleditor import IDF
import eppy.modeleditor as modeleditor


class WhichLoopError(Exception):
    pass


class SomeFields(object):
    """Some fields"""

    c_fields = [
        "Condenser Side Inlet Node Name",
        "Condenser Side Outlet Node Name",
        "Condenser Side Branch List Name",
        "Condenser Side Connector List Name",
        "Demand Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Condenser Demand Side Branch List Name",
        "Condenser Demand Side Connector List Name",
    ]
    p_fields = [
        "Plant Side Inlet Node Name",
        "Plant Side Outlet Node Name",
        "Plant Side Branch List Name",
        "Plant Side Connector List Name",
        "Demand Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Demand Side Branch List Name",
        "Demand Side Connector List Name",
    ]
    a_fields = [
        "Branch List Name",
        "Connector List Name",
        "Supply Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Demand Side Inlet Node Names",
        "Supply Side Outlet Node Names",
    ]


def flattencopy(lst):
    """flatten and return a copy of the list
    indefficient on large lists"""
    # modified from
    # http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    thelist = copy.deepcopy(lst)
    list_is_nested = True
    while list_is_nested:  # outer loop
        keepchecking = False
        atemp = []
        for element in thelist:  # inner loop
            if isinstance(element, list):
                atemp.extend(element)
                keepchecking = True
            else:
                atemp.append(element)
        list_is_nested = keepchecking  # determine if outer loop exits
        thelist = atemp[:]
    return thelist


def makepipecomponent(idf, pname):
    """make a pipe component
    generate inlet outlet names"""
    apipe = idf.newidfobject("Pipe:Adiabatic".upper(), Name=pname)
    apipe.Inlet_Node_Name = "%s_inlet" % (pname,)
    apipe.Outlet_Node_Name = "%s_outlet" % (pname,)
    return apipe


def makeductcomponent(idf, dname):
    """make a duct component
    generate inlet outlet names"""
    aduct = idf.newidfobject("duct".upper(), Name=dname)
    aduct.Inlet_Node_Name = "%s_inlet" % (dname,)
    aduct.Outlet_Node_Name = "%s_outlet" % (dname,)
    return aduct


def makepipebranch(idf, bname):
    """make a branch with a pipe
    use standard inlet outlet names"""
    # make the pipe component first
    pname = "%s_pipe" % (bname,)
    apipe = makepipecomponent(idf, pname)
    # now make the branch with the pipe in it
    abranch = idf.newidfobject("BRANCH", Name=bname)
    abranch.Component_1_Object_Type = "Pipe:Adiabatic"
    abranch.Component_1_Name = pname
    abranch.Component_1_Inlet_Node_Name = apipe.Inlet_Node_Name
    abranch.Component_1_Outlet_Node_Name = apipe.Outlet_Node_Name
    abranch.Component_1_Branch_Control_Type = "Bypass"
    return abranch


def makeductbranch(idf, bname):
    """make a branch with a duct
    use standard inlet outlet names"""
    # make the duct component first
    pname = "%s_duct" % (bname,)
    aduct = makeductcomponent(idf, pname)
    # now make the branch with the duct in it
    abranch = idf.newidfobject("BRANCH", Name=bname)
    abranch.Component_1_Object_Type = "duct"
    abranch.Component_1_Name = pname
    abranch.Component_1_Inlet_Node_Name = aduct.Inlet_Node_Name
    abranch.Component_1_Outlet_Node_Name = aduct.Outlet_Node_Name
    abranch.Component_1_Branch_Control_Type = "Bypass"
    return abranch


def getbranchcomponents(idf, branch, utest=False):
    """get the components of the branch"""
    fobjtype = "Component_%s_Object_Type"
    fobjname = "Component_%s_Name"
    complist = []
    for i in range(1, 100000):
        try:
            objtype = branch[fobjtype % (i,)]
            if objtype.strip() == "":
                break
            objname = branch[fobjname % (i,)]
            complist.append((objtype, objname))
        except bunch_subclass.BadEPFieldError:
            break
    if utest:
        return complist
    else:
        return [idf.getobject(ot, on) for ot, on in complist]


def renamenodes(idf, fieldtype):
    """rename all the changed nodes"""
    renameds = []
    for key in idf.model.dtls:
        for idfobject in idf.idfobjects[key]:
            for fieldvalue in idfobject.obj:
                if type(fieldvalue) is list:
                    if fieldvalue not in renameds:
                        cpvalue = copy.copy(fieldvalue)
                        renameds.append(cpvalue)

    # do the renaming
    for key in idf.model.dtls:
        for idfobject in idf.idfobjects[key]:
            for i, fieldvalue in enumerate(idfobject.obj):
                itsidd = idfobject.objidd[i]
                if "type" in itsidd:
                    if itsidd["type"][0] == fieldtype:
                        tempdct = dict(renameds)
                        if type(fieldvalue) is list:
                            fieldvalue = fieldvalue[-1]
                            idfobject.obj[i] = fieldvalue
                        else:
                            if fieldvalue in tempdct:
                                fieldvalue = tempdct[fieldvalue]
                                idfobject.obj[i] = fieldvalue


def getfieldnamesendswith(idfobject, endswith):
    """get the filednames for the idfobject based on endswith"""
    objls = idfobject.objls
    tmp = [name for name in objls if name.endswith(endswith)]
    if tmp == []:
        pass
    return [name for name in objls if name.endswith(endswith)]


def getnodefieldname(idfobject, endswith, fluid=None, startswith=None):
    """return the field name of the node
    fluid is only needed if there are air and water nodes
    fluid is Air or Water or ''.
    if the fluid is Steam, use Water"""
    if startswith is None:
        startswith = ""
    if fluid is None:
        fluid = ""
    nodenames = getfieldnamesendswith(idfobject, endswith)
    nodenames = [name for name in nodenames if name.startswith(startswith)]
    fnodenames = [nd for nd in nodenames if nd.find(fluid) != -1]
    fnodenames = [name for name in fnodenames if name.startswith(startswith)]
    if len(fnodenames) == 0:
        nodename = nodenames[0]
    else:
        nodename = fnodenames[0]
    return nodename


def connectcomponents(idf, components, fluid=None):
    """rename nodes so that the components get connected
    fluid is only needed if there are air and water nodes
    fluid is Air or Water or ''.
    if the fluid is Steam, use Water"""
    if fluid is None:
        fluid = ""
    if len(components) == 1:
        thiscomp, thiscompnode = components[0]
        initinletoutlet(idf, thiscomp, thiscompnode, force=False)
        outletnodename = getnodefieldname(
            thiscomp, "Outlet_Node_Name", fluid=fluid, startswith=thiscompnode
        )
        thiscomp[outletnodename] = [thiscomp[outletnodename], thiscomp[outletnodename]]
        # inletnodename = getnodefieldname(nextcomp, "Inlet_Node_Name", fluid)
        # nextcomp[inletnodename] = [nextcomp[inletnodename], betweennodename]
        return components
    for i in range(len(components) - 1):
        thiscomp, thiscompnode = components[i]
        nextcomp, nextcompnode = components[i + 1]
        initinletoutlet(idf, thiscomp, thiscompnode, force=False)
        initinletoutlet(idf, nextcomp, nextcompnode, force=False)
        betweennodename = "%s_%s_node" % (thiscomp.Name, nextcomp.Name)
        outletnodename = getnodefieldname(
            thiscomp, "Outlet_Node_Name", fluid=fluid, startswith=thiscompnode
        )
        thiscomp[outletnodename] = [thiscomp[outletnodename], betweennodename]
        inletnodename = getnodefieldname(nextcomp, "Inlet_Node_Name", fluid)
        nextcomp[inletnodename] = [nextcomp[inletnodename], betweennodename]
    return components


def initinletoutlet(idf, idfobject, thisnode, force=False):
    """initialze values for all the inlet outlet nodes for the object.
    if force == False, it willl init only if field = ''"""

    def blankfield(fieldvalue):
        """test for blank field"""
        try:
            if fieldvalue.strip() == "":
                return True
            else:
                return False
        except AttributeError:  # field may be a list
            return False

    def trimfields(fields, thisnode):
        if len(fields) > 1:
            if thisnode is not None:
                fields = [field for field in fields if field.startswith(thisnode)]
                return fields
            else:
                print("Where should this loop connect ?")
                print("%s - %s" % (idfobject.key, idfobject.Name))
                print([field.split("Inlet_Node_Name")[0] for field in inletfields])
                raise WhichLoopError
        else:
            return fields

    inletfields = getfieldnamesendswith(idfobject, "Inlet_Node_Name")
    inletfields = trimfields(inletfields, thisnode)  # or warn with exception
    for inletfield in inletfields:
        if blankfield(idfobject[inletfield]) == True or force == True:
            idfobject[inletfield] = "%s_%s" % (idfobject.Name, inletfield)
    outletfields = getfieldnamesendswith(idfobject, "Outlet_Node_Name")
    outletfields = trimfields(outletfields, thisnode)  # or warn with exception
    for outletfield in outletfields:
        if blankfield(idfobject[outletfield]) == True or force == True:
            idfobject[outletfield] = "%s_%s" % (idfobject.Name, outletfield)
    return idfobject


def componentsintobranch(idf, branch, listofcomponents, fluid=None):
    """insert a list of components into a branch
    fluid is only needed if there are air and water nodes in same object
    fluid is Air or Water or ''.
    if the fluid is Steam, use Water"""
    if fluid is None:
        fluid = ""
    componentlist = [item[0] for item in listofcomponents]
    # assumes that the nodes of the component connect to each other
    # empty branch if it has existing components
    thebranchname = branch.Name
    thebranch = idf.removeextensibles("BRANCH", thebranchname)  # empty the branch
    # fill in the new components with the node names into this branch
    # find the first extensible field and fill in the data in obj.
    e_index = idf.getextensibleindex("BRANCH", thebranchname)
    theobj = thebranch.obj
    modeleditor.extendlist(theobj, e_index)  # just being careful here
    for comp, compnode in listofcomponents:
        theobj.append(comp.key)
        theobj.append(comp.Name)
        inletnodename = getnodefieldname(
            comp, "Inlet_Node_Name", fluid=fluid, startswith=compnode
        )
        theobj.append(comp[inletnodename])
        outletnodename = getnodefieldname(
            comp, "Outlet_Node_Name", fluid=fluid, startswith=compnode
        )
        theobj.append(comp[outletnodename])
        theobj.append("")

    return thebranch


def doingtesting(testing, testn, result=None):
    """doing testing"""
    testn += 1
    if testing == testn:
        print(testing)
        returnnone()
    else:
        return testn


def returnnone():
    """return None"""
    return None


def makeairloop(idf, loopname, sloop, dloop, testing=None):
    """make an airloop"""
    # -------- testing ---------
    testn = 0
    # -------- testing ---------
    newairloop = idf.newidfobject("AirLoopHVAC".upper(), Name=loopname)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    fields = SomeFields.a_fields

    # for use in bunch
    flnames = [field.replace(" ", "_") for field in fields]

    # simplify naming
    fields1 = [
        "Branches",
        "Connectors",
        "Supply Inlet",
        "Demand Outlet",
        "Demand Inlet",
        "Supply Outlet",
    ]

    # old TODO : pop connectors if no parallel branches
    # make fieldnames in the air loop
    fieldnames = ["%s %s" % (loopname, field) for field in fields1]
    for fieldname, thefield in zip(fieldnames, flnames):
        newairloop[thefield] = fieldname
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------

    # make the branch lists for this air loop
    sbranchlist = idf.newidfobject("BRANCHLIST", Name=newairloop[flnames[0]])

    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # add branch names to the branchlist
    sbranchnames = flattencopy(sloop)
    # sbranchnames = sloop[1]
    for branchname in sbranchnames:
        sbranchlist.obj.append(branchname)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # supply side
    sbranchs = []
    for bname in sbranchnames:
        branch = makeductbranch(idf, bname)
        sbranchs.append(branch)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # rename inlet outlet of endpoints of loop
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Supply_Side_Inlet_Node_Name"  # TODO : change ?
    sbranchs[0][anode] = newairloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Supply_Side_Outlet_Node_Names"  # TODO : change ?
    sbranchs[-1][anode] = newairloop[sameoutnode]
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # rename inlet outlet of endpoints of loop - rename in pipe
    dname = sbranchs[0]["Component_1_Name"]  # get the duct name
    aduct = idf.getobject("duct".upper(), dname)  # get duct
    aduct.Inlet_Node_Name = newairloop[sameinnode]
    dname = sbranchs[-1]["Component_1_Name"]  # get the duct name
    aduct = idf.getobject("duct".upper(), dname)  # get duct
    aduct.Outlet_Node_Name = newairloop[sameoutnode]
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    #
    # # TODO : test if there are parallel branches
    # make the connectorlist an fill fields
    sconnlist = idf.newidfobject("CONNECTORLIST", Name=newairloop.Connector_List_Name)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    sconnlist.Connector_1_Object_Type = "Connector:Splitter"
    sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname,)
    sconnlist.Connector_2_Object_Type = "Connector:Mixer"
    sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname,)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # make splitters and mixers
    s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", Name=sconnlist.Connector_1_Name)
    s_splitter.obj.extend([sloop[0]] + sloop[1])
    s_mixer = idf.newidfobject("CONNECTOR:MIXER", Name=sconnlist.Connector_2_Name)
    s_mixer.obj.extend([sloop[-1]] + sloop[1])
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # demand side loop for airloop is made below
    # ZoneHVAC:EquipmentConnections
    for zone in dloop:
        equipconn = idf.newidfobject("ZoneHVAC:EquipmentConnections".upper())
        equipconn.Zone_Name = zone
        fldname = "Zone_Conditioning_Equipment_List_Name"
        equipconn[fldname] = "%s equip list" % (zone,)
        fldname = "Zone_Air_Inlet_Node_or_NodeList_Name"
        equipconn[fldname] = "%s Inlet Node" % (zone,)
        fldname = "Zone_Air_Node_Name"
        equipconn[fldname] = "%s Node" % (zone,)
        fldname = "Zone_Return_Air_Node_Name"
        equipconn[fldname] = "%s Outlet Node" % (zone,)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # make ZoneHVAC:EquipmentList
    for zone in dloop:
        z_equiplst = idf.newidfobject("ZoneHVAC:EquipmentList".upper())
        z_equipconn = modeleditor.getobjects(
            idf.idfobjects,
            idf.model,
            idf.idd_info,
            "ZoneHVAC:EquipmentConnections".upper(),  # places=7,
            **dict(Zone_Name=zone)
        )[0]
        z_equiplst.Name = z_equipconn.Zone_Conditioning_Equipment_List_Name
        fld = "Zone_Equipment_1_Object_Type"
        z_equiplst[fld] = "AirTerminal:SingleDuct:Uncontrolled"
        z_equiplst.Zone_Equipment_1_Name = "%sDirectAir" % (zone,)
        z_equiplst.Zone_Equipment_1_Cooling_Sequence = 1
        z_equiplst.Zone_Equipment_1_Heating_or_NoLoad_Sequence = 1
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # make AirTerminal:SingleDuct:Uncontrolled
    for zone in dloop:
        z_equipconn = modeleditor.getobjects(
            idf.idfobjects,
            idf.model,
            idf.idd_info,
            "ZoneHVAC:EquipmentConnections".upper(),  # places=7,
            **dict(Zone_Name=zone)
        )[0]
        key = "AirTerminal:SingleDuct:Uncontrolled".upper()
        z_airterm = idf.newidfobject(key)
        z_airterm.Name = "%sDirectAir" % (zone,)
        fld1 = "Zone_Supply_Air_Node_Name"
        fld2 = "Zone_Air_Inlet_Node_or_NodeList_Name"
        z_airterm[fld1] = z_equipconn[fld2]
        z_airterm.Maximum_Air_Flow_Rate = "autosize"
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # MAKE AirLoopHVAC:ZoneSplitter
    # zone = dloop[0]
    key = "AirLoopHVAC:ZoneSplitter".upper()
    z_splitter = idf.newidfobject(key)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    z_splitter.Name = "%s Demand Side Splitter" % (loopname,)
    z_splitter.Inlet_Node_Name = newairloop.Demand_Side_Inlet_Node_Names
    for i, zone in enumerate(dloop):
        z_equipconn = modeleditor.getobjects(
            idf.idfobjects,
            idf.model,
            idf.idd_info,
            "ZoneHVAC:EquipmentConnections".upper(),  # places=7,
            **dict(Zone_Name=zone)
        )[0]
        fld = "Outlet_%s_Node_Name" % (i + 1,)
        z_splitter[fld] = z_equipconn.Zone_Air_Inlet_Node_or_NodeList_Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # make AirLoopHVAC:SupplyPath
    key = "AirLoopHVAC:SupplyPath".upper()
    z_supplypth = idf.newidfobject(key)
    z_supplypth.Name = "%sSupplyPath" % (loopname,)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    fld1 = "Supply_Air_Path_Inlet_Node_Name"
    fld2 = "Demand_Side_Inlet_Node_Names"
    z_supplypth[fld1] = newairloop[fld2]
    z_supplypth.Component_1_Object_Type = "AirLoopHVAC:ZoneSplitter"
    z_supplypth.Component_1_Name = z_splitter.Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # make AirLoopHVAC:ZoneMixer
    key = "AirLoopHVAC:ZoneMixer".upper()
    z_mixer = idf.newidfobject(key)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    z_mixer.Name = "%s Demand Side Mixer" % (loopname,)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    z_mixer.Outlet_Node_Name = newairloop.Demand_Side_Outlet_Node_Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    for i, zone in enumerate(dloop):
        z_equipconn = modeleditor.getobjects(
            idf.idfobjects,
            idf.model,
            idf.idd_info,
            "ZoneHVAC:EquipmentConnections".upper(),  # places=7,
            **dict(Zone_Name=zone)
        )[0]
        fld = "Inlet_%s_Node_Name" % (i + 1,)
        z_mixer[fld] = z_equipconn.Zone_Return_Air_Node_Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    # make AirLoopHVAC:ReturnPath
    key = "AirLoopHVAC:ReturnPath".upper()
    z_returnpth = idf.newidfobject(key)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    z_returnpth.Name = "%sReturnPath" % (loopname,)
    z_returnpth.Return_Air_Path_Outlet_Node_Name = (
        newairloop.Demand_Side_Outlet_Node_Name
    )
    z_returnpth.Component_1_Object_Type = "AirLoopHVAC:ZoneMixer"
    z_returnpth.Component_1_Name = z_mixer.Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None:
        returnnone()
    # -------- testing ---------
    return newairloop


def makeplantloop(idf, loopname, sloop, dloop, testing=None):
    """make plant loop with pip components"""
    # -------- <testing ---------
    testn = 0
    # -------- testing> ---------
    newplantloop = idf.newidfobject("PLANTLOOP", Name=loopname)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    fields = SomeFields.p_fields

    # for use in bunch
    flnames = [field.replace(" ", "_") for field in fields]

    # simplify naming
    fields1 = [field.replace("Plant Side", "Supply") for field in fields]
    fields1 = [field.replace("Demand Side", "Demand") for field in fields1]
    fields1 = [field[: field.find("Name") - 1] for field in fields1]
    fields1 = [field.replace(" Node", "") for field in fields1]
    fields1 = [field.replace(" List", "s") for field in fields1]

    # TODO : pop connectors if no parallel branches
    # make fieldnames in the plant loop
    fieldnames = ["%s %s" % (loopname, field) for field in fields1]
    for fieldname, thefield in zip(fieldnames, flnames):
        newplantloop[thefield] = fieldname
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # make the branch lists for this plant loop
    sbranchlist = idf.newidfobject(
        "BRANCHLIST", Name=newplantloop.Plant_Side_Branch_List_Name
    )
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    dbranchlist = idf.newidfobject(
        "BRANCHLIST", Name=newplantloop.Demand_Side_Branch_List_Name
    )
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # add branch names to the branchlist
    sbranchnames = flattencopy(sloop)
    # sbranchnames = sloop[1]
    for branchname in sbranchnames:
        sbranchlist.obj.append(branchname)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    dbranchnames = flattencopy(dloop)
    # dbranchnames = dloop[1]
    for branchname in dbranchnames:
        dbranchlist.obj.append(branchname)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # make a pipe branch for all branches in the loop

    # supply side
    sbranchs = []
    for bname in sbranchnames:
        branch = makepipebranch(idf, bname)
        sbranchs.append(branch)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Plant_Side_Inlet_Node_Name"
    sbranchs[0][anode] = newplantloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Plant_Side_Outlet_Node_Name"
    sbranchs[-1][anode] = newplantloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = sbranchs[0]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Inlet_Node_Name = newplantloop[sameinnode]
    pname = sbranchs[-1]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Outlet_Node_Name = newplantloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # demand side
    dbranchs = []
    for bname in dbranchnames:
        branch = makepipebranch(idf, bname)
        dbranchs.append(branch)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop - rename in branch
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Demand_Side_Inlet_Node_Name"
    dbranchs[0][anode] = newplantloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Demand_Side_Outlet_Node_Name"
    dbranchs[-1][anode] = newplantloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = dbranchs[0]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Inlet_Node_Name = newplantloop[sameinnode]
    pname = dbranchs[-1]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Outlet_Node_Name = newplantloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # TODO : test if there are parallel branches
    # make the connectorlist an fill fields
    sconnlist = idf.newidfobject(
        "CONNECTORLIST", Name=newplantloop.Plant_Side_Connector_List_Name
    )
    sconnlist.Connector_1_Object_Type = "Connector:Splitter"
    sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname,)
    sconnlist.Connector_2_Object_Type = "Connector:Mixer"
    sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname,)
    dconnlist = idf.newidfobject(
        "CONNECTORLIST", Name=newplantloop.Demand_Side_Connector_List_Name
    )
    dconnlist.Connector_1_Object_Type = "Connector:Splitter"
    dconnlist.Connector_1_Name = "%s_demand_splitter" % (loopname,)
    dconnlist.Connector_2_Object_Type = "Connector:Mixer"
    dconnlist.Connector_2_Name = "%s_demand_mixer" % (loopname,)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # make splitters and mixers
    s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", Name=sconnlist.Connector_1_Name)
    s_splitter.obj.extend([sloop[0]] + sloop[1])
    s_mixer = idf.newidfobject("CONNECTOR:MIXER", Name=sconnlist.Connector_2_Name)
    s_mixer.obj.extend([sloop[-1]] + sloop[1])
    # -
    d_splitter = idf.newidfobject("CONNECTOR:SPLITTER", Name=dconnlist.Connector_1_Name)
    d_splitter.obj.extend([dloop[0]] + dloop[1])
    d_mixer = idf.newidfobject("CONNECTOR:MIXER", Name=dconnlist.Connector_2_Name)
    d_mixer.obj.extend([dloop[-1]] + dloop[1])
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newplantloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    return newplantloop


def makecondenserloop(idf, loopname, sloop, dloop, testing=None):
    """make condenser loop with pipe components"""
    # -------- <testing ---------
    testn = 0
    # -------- testing> ---------
    newcondenserloop = idf.newidfobject("CondenserLoop".upper(), Name=loopname)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    fields = SomeFields.c_fields

    # for use in bunch
    flnames = [field.replace(" ", "_") for field in fields]

    # simplify naming
    fields1 = [field.replace("Condenser Side", "Cond_Supply") for field in fields]
    fields1 = [field.replace("Demand Side", "Demand") for field in fields1]
    fields1 = [field[: field.find("Name") - 1] for field in fields1]
    fields1 = [field.replace(" Node", "") for field in fields1]
    fields1 = [field.replace(" List", "s") for field in fields1]

    # old TODO : pop connectors if no parallel branches
    # make fieldnames in the condenser loop
    fieldnames = ["%s %s" % (loopname, field) for field in fields1]
    for fieldname, thefield in zip(fieldnames, flnames):
        newcondenserloop[thefield] = fieldname
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # make the branch lists for this condenser loop
    sbranchlist = idf.newidfobject(
        "BRANCHLIST", Name=newcondenserloop.Condenser_Side_Branch_List_Name
    )
    dbranchlist = idf.newidfobject(
        "BRANCHLIST", Name=newcondenserloop.Condenser_Demand_Side_Branch_List_Name
    )
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # add branch names to the branchlist
    sbranchnames = flattencopy(sloop)
    # sbranchnames = sloop[1]
    for branchname in sbranchnames:
        sbranchlist.obj.append(branchname)
    dbranchnames = flattencopy(dloop)
    # dbranchnames = dloop[1]
    for branchname in dbranchnames:
        dbranchlist.obj.append(branchname)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # make a pipe branch for all branches in the loop

    # supply side
    sbranchs = []
    for bname in sbranchnames:
        branch = makepipebranch(idf, bname)
        sbranchs.append(branch)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Condenser_Side_Inlet_Node_Name"  # TODO : change ?
    sbranchs[0][anode] = newcondenserloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Condenser_Side_Outlet_Node_Name"  # TODO : change ?
    sbranchs[-1][anode] = newcondenserloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = sbranchs[0]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Inlet_Node_Name = newcondenserloop[sameinnode]
    pname = sbranchs[-1]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Outlet_Node_Name = newcondenserloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # demand side
    dbranchs = []
    for bname in dbranchnames:
        branch = makepipebranch(idf, bname)
        dbranchs.append(branch)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop - rename in branch
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Demand_Side_Inlet_Node_Name"  # TODO : change ?
    dbranchs[0][anode] = newcondenserloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Demand_Side_Outlet_Node_Name"  # TODO : change ?
    dbranchs[-1][anode] = newcondenserloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = dbranchs[0]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Inlet_Node_Name = newcondenserloop[sameinnode]
    pname = dbranchs[-1]["Component_1_Name"]  # get the pipe name
    apipe = idf.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
    apipe.Outlet_Node_Name = newcondenserloop[sameoutnode]
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # TODO : test if there are parallel branches
    # make the connectorlist an fill fields
    sconnlist = idf.newidfobject(
        "CONNECTORLIST", Name=newcondenserloop.Condenser_Side_Connector_List_Name
    )
    sconnlist.Connector_1_Object_Type = "Connector:Splitter"
    sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname,)
    sconnlist.Connector_2_Object_Type = "Connector:Mixer"
    sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname,)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    dconnlist = idf.newidfobject(
        "CONNECTORLIST", Name=newcondenserloop.Condenser_Demand_Side_Connector_List_Name
    )
    dconnlist.Connector_1_Object_Type = "Connector:Splitter"
    dconnlist.Connector_1_Name = "%s_demand_splitter" % (loopname,)
    dconnlist.Connector_2_Object_Type = "Connector:Mixer"
    dconnlist.Connector_2_Name = "%s_demand_mixer" % (loopname,)
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------

    # make splitters and mixers
    s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", Name=sconnlist.Connector_1_Name)
    s_splitter.obj.extend([sloop[0]] + sloop[1])
    s_mixer = idf.newidfobject("CONNECTOR:MIXER", Name=sconnlist.Connector_2_Name)
    s_mixer.obj.extend([sloop[-1]] + sloop[1])
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    # -
    d_splitter = idf.newidfobject("CONNECTOR:SPLITTER", Name=dconnlist.Connector_1_Name)
    d_splitter.obj.extend([dloop[0]] + dloop[1])
    d_mixer = idf.newidfobject("CONNECTOR:MIXER", Name=dconnlist.Connector_2_Name)
    d_mixer.obj.extend([dloop[-1]] + dloop[1])
    # -------- <testing ---------
    testn = doingtesting(testing, testn, newcondenserloop)
    if testn == None:
        returnnone()
    # -------- testing> ---------
    return newcondenserloop


def _clean_listofcomponents(listofcomponents):
    """force it to be a list of tuples"""

    def totuple(item):
        """return a tuple"""
        if isinstance(item, (tuple, list)):
            return item
        else:
            return (item, None)

    return [totuple(item) for item in listofcomponents]


def _clean_listofcomponents_tuples(listofcomponents_tuples):
    """force 3 items in the tuple"""

    def to3tuple(item):
        """return a 3 item tuple"""
        if len(item) == 3:
            return item
        else:
            return (item[0], item[1], None)

    return [to3tuple(item) for item in listofcomponents_tuples]


def getmakeidfobject(idf, key, name):
    """get idfobject or make it if it does not exist"""
    idfobject = idf.getobject(key, name)
    if not idfobject:
        return idf.newidfobject(key, Name=name)
    else:
        return idfobject


def replacebranch1(
    idf, loop, branchname, listofcomponents_tuples, fluid=None, debugsave=False
):
    """do I even use this ? .... yup! I do"""
    if fluid is None:
        fluid = ""
    listofcomponents_tuples = _clean_listofcomponents_tuples(listofcomponents_tuples)
    branch = idf.getobject("BRANCH", branchname)  # args are (key, name)
    listofcomponents = []
    for comp_type, comp_name, compnode in listofcomponents_tuples:
        comp = getmakeidfobject(idf, comp_type.upper(), comp_name)
        listofcomponents.append((comp, compnode))
    newbr = replacebranch(
        idf, loop, branch, listofcomponents, debugsave=debugsave, fluid=fluid
    )
    return newbr


def replacebranch(
    idf, loop, branch, listofcomponents, fluid=None, debugsave=False, testing=None
):
    """It will replace the components in the branch with components in
    listofcomponents"""
    if fluid is None:
        fluid = ""
    # -------- testing ---------
    testn = 0
    # -------- testing ---------

    # join them into a branch
    # -----------------------
    # np1_inlet -> np1 -> np1_np2_node -> np2 -> np2_outlet
    # change the node names in the component
    # empty the old branch
    # fill in the new components with the node names into this branch
    listofcomponents = _clean_listofcomponents(listofcomponents)

    components = [item[0] for item in listofcomponents]
    connectcomponents(idf, listofcomponents, fluid=fluid)
    if debugsave:
        idf.savecopy("hhh3.idf")
    # -------- testing ---------
    testn = doingtesting(testing, testn)
    if testn == None:
        returnnone()
    # -------- testing ---------
    fields = SomeFields.a_fields

    thebranch = branch
    componentsintobranch(idf, thebranch, listofcomponents, fluid=fluid)
    if debugsave:
        idf.savecopy("hhh4.idf")
    # -------- testing ---------
    testn = doingtesting(testing, testn)
    if testn == None:
        returnnone()
    # -------- testing ---------

    # # gather all renamed nodes
    # # do the renaming
    renamenodes(idf, "node")
    if debugsave:
        idf.savecopy("hhh7.idf")
    # -------- testing ---------
    testn = doingtesting(testing, testn)
    if testn == None:
        returnnone()
    # -------- testing ---------

    # check for the end nodes of the loop
    if loop.key == "AIRLOOPHVAC":
        fields = SomeFields.a_fields
    if loop.key == "PLANTLOOP":
        fields = SomeFields.p_fields
    if loop.key == "CONDENSERLOOP":
        fields = SomeFields.c_fields
    # for use in bunch
    flnames = [field.replace(" ", "_") for field in fields]

    if fluid.upper() == "WATER":
        supplyconlistname = loop[flnames[3]]
        # Plant_Side_Connector_List_Name or Condenser_Side_Connector_List_Name
    elif fluid.upper() == "AIR":
        supplyconlistname = loop[flnames[1]]  # Connector_List_Name'
    supplyconlist = idf.getobject("CONNECTORLIST", supplyconlistname)
    for i in range(1, 100000):  # large range to hit end
        try:
            fieldname = "Connector_%s_Object_Type" % (i,)
            ctype = supplyconlist[fieldname]
        except bunch_subclass.BadEPFieldError:
            break
        if ctype.strip() == "":
            break
        fieldname = "Connector_%s_Name" % (i,)
        cname = supplyconlist[fieldname]
        connector = idf.getobject(ctype.upper(), cname)
        if connector.key == "CONNECTOR:SPLITTER":
            firstbranchname = connector.Inlet_Branch_Name
            cbranchname = firstbranchname
            isfirst = True
        if connector.key == "CONNECTOR:MIXER":
            lastbranchname = connector.Outlet_Branch_Name
            cbranchname = lastbranchname
            isfirst = False
        if cbranchname == thebranch.Name:
            # rename end nodes
            comps = getbranchcomponents(idf, thebranch)
            if isfirst:
                comp = comps[0]
                inletnodename = getnodefieldname(comp, "Inlet_Node_Name", fluid)
                comp[inletnodename] = [
                    comp[inletnodename],
                    loop[flnames[0]],
                ]  # Plant_Side_Inlet_Node_Name
            else:
                comp = comps[-1]
                outletnodename = getnodefieldname(comp, "Outlet_Node_Name", fluid)
                comp[outletnodename] = [
                    comp[outletnodename],
                    loop[flnames[1]],
                ]  # .Plant_Side_Outlet_Node_Name
    # -------- testing ---------
    testn = doingtesting(testing, testn)
    if testn == None:
        returnnone()
    # -------- testing ---------

    if fluid.upper() == "WATER":
        demandconlistname = loop[flnames[7]]  # .Demand_Side_Connector_List_Name
        demandconlist = idf.getobject("CONNECTORLIST", demandconlistname)
        for i in range(1, 100000):  # large range to hit end
            try:
                fieldname = "Connector_%s_Object_Type" % (i,)
                ctype = demandconlist[fieldname]
            except bunch_subclass.BadEPFieldError:
                break
            if ctype.strip() == "":
                break
            fieldname = "Connector_%s_Name" % (i,)
            cname = demandconlist[fieldname]
            connector = idf.getobject(ctype.upper(), cname)
            if connector.key == "CONNECTOR:SPLITTER":
                firstbranchname = connector.Inlet_Branch_Name
                cbranchname = firstbranchname
                isfirst = True
            if connector.key == "CONNECTOR:MIXER":
                lastbranchname = connector.Outlet_Branch_Name
                cbranchname = lastbranchname
                isfirst = False
            if cbranchname == thebranch.Name:
                # rename end nodes
                comps = getbranchcomponents(idf, thebranch)
                if isfirst:
                    comp = comps[0]
                    inletnodename = getnodefieldname(comp, "Inlet_Node_Name", fluid)
                    comp[inletnodename] = [
                        comp[inletnodename],
                        loop[flnames[4]],
                    ]  # .Demand_Side_Inlet_Node_Name
                if not isfirst:
                    comp = comps[-1]
                    outletnodename = getnodefieldname(comp, "Outlet_Node_Name", fluid)
                    comp[outletnodename] = [
                        comp[outletnodename],
                        loop[flnames[5]],
                    ]  # .Demand_Side_Outlet_Node_Name

    # -------- testing ---------
    testn = doingtesting(testing, testn)
    if testn == None:
        returnnone()
    # -------- testing ---------

    if debugsave:
        idf.savecopy("hhh8.idf")

    # # gather all renamed nodes
    # # do the renaming
    renamenodes(idf, "node")
    # -------- testing ---------
    testn = doingtesting(testing, testn)
    if testn == None:
        returnnone()
    # -------- testing ---------
    if debugsave:
        idf.savecopy("hhh9.idf")
    return thebranch


def main():
    """the main routine"""
    from io import StringIO
    import eppy.iddv7 as iddv7

    IDF.setiddname(StringIO(iddv7.iddtxt))
    idf1 = IDF(StringIO(""))
    loopname = "p_loop"
    sloop = ["sb0", ["sb1", "sb2", "sb3"], "sb4"]
    dloop = ["db0", ["db1", "db2", "db3"], "db4"]
    # makeplantloop(idf1, loopname, sloop, dloop)
    loopname = "c_loop"
    sloop = ["sb0", ["sb1", "sb2", "sb3"], "sb4"]
    dloop = ["db0", ["db1", "db2", "db3"], "db4"]
    # makecondenserloop(idf1, loopname, sloop, dloop)
    loopname = "a_loop"
    sloop = ["sb0", ["sb1", "sb2", "sb3"], "sb4"]
    dloop = ["zone1", "zone2", "zone3"]
    makeairloop(idf1, loopname, sloop, dloop)
    idf1.savecopy("hh1.idf")


if __name__ == "__main__":
    main()
