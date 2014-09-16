def makeplantloop(idf, loopname, sloop, dloop):
    """make plant loop with pip components"""
    newplantloop = idf.newidfobject("PLANTLOOP", loopname)
    fields = SomeFields.p_fields

    # for use in bunch
    flnames = [field.replace(' ', '_') for field in fields]

    # implify naming
    fields1 = [field.replace('Plant Side', 'Supply') for field in fields]
    fields1 = [field.replace('Demand Side', 'Demand') for field in fields1]
    fields1 = [field[:field.find('Name') - 1] for field in fields1]
    fields1 = [field.replace(' Node', '') for field in fields1]
    fields1 = [field.replace(' List', 's') for field in fields1]

    # TODO : pop connectors if no parallel branches
    # make fieldnames in the plant loop
    fieldnames = ['%s %s' % (loopname, field) for field in fields1]
    for fieldname, thefield in zip(fieldnames, flnames):
        newplantloop[thefield] = fieldname
    
    # make the branch lists for this plant loop    
    sbranchlist = idf.newidfobject("BRANCHLIST",
                    newplantloop.Plant_Side_Branch_List_Name)
    dbranchlist = idf.newidfobject("BRANCHLIST",
                    newplantloop.Demand_Side_Branch_List_Name)

    # add branch names to the branchlist
    sbranchnames = flattencopy(sloop)
    # sbranchnames = sloop[1]
    for branchname in sbranchnames:
        sbranchlist.obj.append(branchname)
    dbranchnames = flattencopy(dloop)
    # dbranchnames = dloop[1]
    for branchname in dbranchnames:
        dbranchlist.obj.append(branchname)

    # make a pipe branch for all branches in the loop

    # supply side
    sbranchs = []
    for bname in sbranchnames:
        branch = makepipebranch(idf, bname)
        sbranchs.append(branch)
    # rename inlet outlet of endpoints of loop
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Plant_Side_Inlet_Node_Name"
    sbranchs[0][anode] =  newplantloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Plant_Side_Outlet_Node_Name"
    sbranchs[-1][anode] =  newplantloop[sameoutnode]
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = sbranchs[0]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Inlet_Node_Name = newplantloop[sameinnode]
    pname = sbranchs[-1]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Outlet_Node_Name = newplantloop[sameoutnode]

    # demand side
    dbranchs = []
    for bname in dbranchnames:
        branch = makepipebranch(idf, bname)
        dbranchs.append(branch)
    # rename inlet outlet of endpoints of loop - rename in branch
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Demand_Side_Inlet_Node_Name"
    dbranchs[0][anode] =  newplantloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Demand_Side_Outlet_Node_Name"
    dbranchs[-1][anode] =  newplantloop[sameoutnode]
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = dbranchs[0]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Inlet_Node_Name = newplantloop[sameinnode]
    pname = dbranchs[-1]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Outlet_Node_Name = newplantloop[sameoutnode]


    # TODO : test if there are parallel branches
    # make the connectorlist an fill fields
    sconnlist = idf.newidfobject("CONNECTORLIST",
                    newplantloop.Plant_Side_Connector_List_Name)
    sconnlist.Connector_1_Object_Type = "Connector:Splitter"
    sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname, )
    sconnlist.Connector_2_Object_Type = "Connector:Mixer"
    sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname, )
    dconnlist = idf.newidfobject("CONNECTORLIST",
                    newplantloop.Demand_Side_Connector_List_Name)
    dconnlist.Connector_1_Object_Type = "Connector:Splitter"
    dconnlist.Connector_1_Name = "%s_demand_splitter" % (loopname, )
    dconnlist.Connector_2_Object_Type = "Connector:Mixer"
    dconnlist.Connector_2_Name = "%s_demand_mixer" % (loopname, )

    # make splitters and mixers
    s_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
        sconnlist.Connector_1_Name)
    s_splitter.obj.extend([sloop[0]] + sloop[1])
    s_mixer = idf.newidfobject("CONNECTOR:MIXER", 
        sconnlist.Connector_2_Name)
    s_mixer.obj.extend([sloop[-1]] + sloop[1])
    # -
    d_splitter = idf.newidfobject("CONNECTOR:SPLITTER", 
        dconnlist.Connector_1_Name)
    d_splitter.obj.extend([dloop[0]] + dloop[1])
    d_mixer = idf.newidfobject("CONNECTOR:MIXER", 
        dconnlist.Connector_2_Name)
    d_mixer.obj.extend([dloop[-1]] + dloop[1])
    return newplantloop

