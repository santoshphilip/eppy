def doingtesting(testing, testn, result):
    testn += 1
    if testing == testn:
        print testing
        return None
    else:
        return testn
                
def makeairloop1(idf, loopname, sloop, dloop, testing=None):
    """make an airloop"""
    # -------- testing ---------
    testn = 0
    # -------- testing ---------    
    newairloop = idf.newidfobject("AirLoopHVAC".upper(), loopname)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    fields = SomeFields.a_fields

    # for use in bunch
    flnames = [field.replace(' ', '_') for field in fields]

    # simplify naming
    fields1 = ['Branches',
     'Connectors',
     'Supply Inlet',
     'Demand Outlet',
     'Demand Inlet',
     'Supply Outlet'] 

    # old TODO : pop connectors if no parallel branches
    # make fieldnames in the air loop
    fieldnames = ['%s %s' % (loopname, field) for field in fields1]
    for fieldname, thefield in zip(fieldnames, flnames):
        newairloop[thefield] = fieldname
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------

    # make the branch lists for this air loop    
    sbranchlist = idf.newidfobject("BRANCHLIST",
                    newairloop[flnames[0]])

    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # add branch names to the branchlist
    sbranchnames = flattencopy(sloop)
    # sbranchnames = sloop[1]
    for branchname in sbranchnames:
        sbranchlist.obj.append(branchname)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # supply side
    sbranchs = []
    for bname in sbranchnames:
        branch = makeductbranch(idf, bname)
        sbranchs.append(branch)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # rename inlet outlet of endpoints of loop
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Supply_Side_Inlet_Node_Name" # TODO : change ?
    sbranchs[0][anode] =  newairloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Supply_Side_Outlet_Node_Names" # TODO : change ?
    sbranchs[-1][anode] =  newairloop[sameoutnode]
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # rename inlet outlet of endpoints of loop - rename in pipe
    dname = sbranchs[0]['Component_1_Name'] # get the duct name
    aduct = idf.getobject('duct'.upper(), dname) # get duct
    aduct.Inlet_Node_Name = newairloop[sameinnode]
    dname = sbranchs[-1]['Component_1_Name'] # get the duct name
    aduct = idf.getobject('duct'.upper(), dname) # get duct
    aduct.Outlet_Node_Name = newairloop[sameoutnode]
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # 
    # # TODO : test if there are parallel branches
    # make the connectorlist an fill fields
    sconnlist = idf.newidfobject("CONNECTORLIST",
                    newairloop.Connector_List_Name)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    sconnlist.Connector_1_Object_Type = "Connector:Splitter"
    sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname, )
    sconnlist.Connector_2_Object_Type = "Connector:Mixer"
    sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname, )
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # make splitters and mixers
    s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
        sconnlist.Connector_1_Name)
    s_splitter.obj.extend([sloop[0]] + sloop[1])
    s_mixer = idf.newidfobject("CONNECTOR:MIXER", 
        sconnlist.Connector_2_Name)
    s_mixer.obj.extend([sloop[-1]] + sloop[1])
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # demand side loop for airloop is made below 
    #ZoneHVAC:EquipmentConnections
    for zone in dloop:
        equipconn = idf.newidfobject("ZoneHVAC:EquipmentConnections".upper())
        equipconn.Zone_Name = zone
        fldname = "Zone_Conditioning_Equipment_List_Name"
        equipconn[fldname] = "%s equip list" % (zone, )
        fldname = "Zone_Air_Inlet_Node_or_NodeList_Name"
        equipconn[fldname] = "%s Inlet Node" % (zone, )
        fldname = "Zone_Air_Node_Name"
        equipconn[fldname] = "%s Node" % (zone, )
        fldname = "Zone_Return_Air_Node_Name"
        equipconn[fldname] = "%s Outlet Node" % (zone, )
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # make ZoneHVAC:EquipmentList
    for zone in dloop:
        z_equiplst = idf.newidfobject("ZoneHVAC:EquipmentList".upper())
        z_equipconn = modeleditor.getobjects(idf.idfobjects, 
            idf.model, idf.idd_info, 
            "ZoneHVAC:EquipmentConnections".upper(), #places=7,
            **dict(Zone_Name=zone))[0]
        z_equiplst.Name = z_equipconn.Zone_Conditioning_Equipment_List_Name
        fld = "Zone_Equipment_1_Object_Type"
        z_equiplst[fld] = "AirTerminal:SingleDuct:Uncontrolled"
        z_equiplst.Zone_Equipment_1_Name = "%sDirectAir" % (zone, )
        z_equiplst.Zone_Equipment_1_Cooling_Sequence = 1
        z_equiplst.Zone_Equipment_1_Heating_or_NoLoad_Sequence = 1
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # make AirTerminal:SingleDuct:Uncontrolled
    for zone in dloop:
        z_equipconn = modeleditor.getobjects(idf.idfobjects, 
            idf.model, idf.idd_info, 
            "ZoneHVAC:EquipmentConnections".upper(), #places=7,
            **dict(Zone_Name=zone))[0]
        key = "AirTerminal:SingleDuct:Uncontrolled".upper()
        z_airterm = idf.newidfobject(key)
        z_airterm.Name = "%sDirectAir" % (zone, )
        fld1 = "Zone_Supply_Air_Node_Name"
        fld2 = "Zone_Air_Inlet_Node_or_NodeList_Name"
        z_airterm[fld1] = z_equipconn[fld2]
        z_airterm.Maximum_Air_Flow_Rate = 'autosize'
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # MAKE AirLoopHVAC:ZoneSplitter
    # zone = dloop[0]
    key = "AirLoopHVAC:ZoneSplitter".upper()
    z_splitter = idf.newidfobject(key)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    z_splitter.Name = "%s Demand Side Splitter" % (loopname, )
    z_splitter.Inlet_Node_Name = newairloop.Demand_Side_Inlet_Node_Names
    for i, zone in enumerate(dloop):
        z_equipconn = modeleditor.getobjects(idf.idfobjects, 
            idf.model, idf.idd_info, 
            "ZoneHVAC:EquipmentConnections".upper(), #places=7,
            **dict(Zone_Name=zone))[0]
        fld = "Outlet_%s_Node_Name" % (i + 1, )
        z_splitter[fld] = z_equipconn.Zone_Air_Inlet_Node_or_NodeList_Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # make AirLoopHVAC:SupplyPath
    key = "AirLoopHVAC:SupplyPath".upper()
    z_supplypth = idf.newidfobject(key)
    z_supplypth.Name = "%sSupplyPath" % (loopname, )
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    fld1 = "Supply_Air_Path_Inlet_Node_Name"
    fld2 = "Demand_Side_Inlet_Node_Names"
    z_supplypth[fld1] = newairloop[fld2]
    z_supplypth.Component_1_Object_Type = "AirLoopHVAC:ZoneSplitter"
    z_supplypth.Component_1_Name = z_splitter.Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # make AirLoopHVAC:ZoneMixer
    key = "AirLoopHVAC:ZoneMixer".upper()
    z_mixer = idf.newidfobject(key)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    z_mixer.Name = "%s Demand Side Mixer" % (loopname, )
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    z_mixer.Outlet_Node_Name = newairloop.Demand_Side_Outlet_Node_Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    for i, zone in enumerate(dloop):
        z_equipconn = modeleditor.getobjects(idf.idfobjects, 
            idf.model, idf.idd_info, 
            "ZoneHVAC:EquipmentConnections".upper(), #places=7,
            **dict(Zone_Name=zone))[0]
        fld = "Inlet_%s_Node_Name" % (i + 1, )
        z_mixer[fld] = z_equipconn.Zone_Return_Air_Node_Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    # make AirLoopHVAC:ReturnPath
    key = "AirLoopHVAC:ReturnPath".upper()
    z_returnpth = idf.newidfobject(key)
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    z_returnpth.Name = "%sReturnPath" % (loopname, )
    z_returnpth.Return_Air_Path_Outlet_Node_Name = newairloop.Demand_Side_Outlet_Node_Name
    z_returnpth.Component_1_Object_Type = "AirLoopHVAC:ZoneMixer"
    z_returnpth.Component_1_Name = z_mixer.Name
    # -------- testing ---------
    testn = doingtesting(testing, testn, newairloop)
    if testn == None: return newairloop
    # -------- testing ---------
    return newairloop
