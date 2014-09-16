def makecondenserloop(idf, loopname, sloop, dloop):
    """make condenser loop with pipe components"""

    newcondenserloop = idf.newidfobject("CondenserLoop".upper(), loopname)

    fields = SomeFields.c_fields

    # for use in bunch
    flnames = [field.replace(' ', '_') for field in fields]

    # simplify naming
    fields1 = [field.replace('Condenser Side', 
                                    'Cond_Supply') for field in fields]
    fields1 = [field.replace('Demand Side', 'Demand') for field in fields1]
    fields1 = [field[:field.find('Name') - 1] for field in fields1]
    fields1 = [field.replace(' Node', '') for field in fields1]
    fields1 = [field.replace(' List', 's') for field in fields1]

    # old TODO : pop connectors if no parallel branches
    # make fieldnames in the condenser loop
    fieldnames = ['%s %s' % (loopname, field) for field in fields1]
    for fieldname, thefield in zip(fieldnames, flnames):
        newcondenserloop[thefield] = fieldname
    
    # make the branch lists for this condenser loop    
    sbranchlist = idf.newidfobject("BRANCHLIST",
                    newcondenserloop.Condenser_Side_Branch_List_Name)
    dbranchlist = idf.newidfobject("BRANCHLIST",
                    newcondenserloop.Condenser_Demand_Side_Branch_List_Name)

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
    sameinnode = "Condenser_Side_Inlet_Node_Name" # TODO : change ?
    sbranchs[0][anode] =  newcondenserloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Condenser_Side_Outlet_Node_Name" # TODO : change ?
    sbranchs[-1][anode] =  newcondenserloop[sameoutnode]
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = sbranchs[0]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Inlet_Node_Name = newcondenserloop[sameinnode]
    pname = sbranchs[-1]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Outlet_Node_Name = newcondenserloop[sameoutnode]

    # demand side
    dbranchs = []
    for bname in dbranchnames:
        branch = makepipebranch(idf, bname)
        dbranchs.append(branch)
    # rename inlet outlet of endpoints of loop - rename in branch
    anode = "Component_1_Inlet_Node_Name"
    sameinnode = "Demand_Side_Inlet_Node_Name" # TODO : change ?
    dbranchs[0][anode] =  newcondenserloop[sameinnode]
    anode = "Component_1_Outlet_Node_Name"
    sameoutnode = "Demand_Side_Outlet_Node_Name" # TODO : change ?
    dbranchs[-1][anode] =  newcondenserloop[sameoutnode]
    # rename inlet outlet of endpoints of loop - rename in pipe
    pname = dbranchs[0]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Inlet_Node_Name = newcondenserloop[sameinnode]
    pname = dbranchs[-1]['Component_1_Name'] # get the pipe name
    apipe = idf.getobject('Pipe:Adiabatic'.upper(), pname) # get pipe
    apipe.Outlet_Node_Name = newcondenserloop[sameoutnode]


    # TODO : test if there are parallel branches
    # make the connectorlist an fill fields
    sconnlist = idf.newidfobject("CONNECTORLIST",
                    newcondenserloop.Condenser_Side_Connector_List_Name)
    sconnlist.Connector_1_Object_Type = "Connector:Splitter"
    sconnlist.Connector_1_Name = "%s_supply_splitter" % (loopname, )
    sconnlist.Connector_2_Object_Type = "Connector:Mixer"
    sconnlist.Connector_2_Name = "%s_supply_mixer" % (loopname, )
    dconnlist = idf.newidfobject("CONNECTORLIST",
        newcondenserloop.Condenser_Demand_Side_Connector_List_Name)
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
    return newcondenserloop

