# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for hvacbuilder"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import StringIO

import eppy.hvacbuilder as hvacbuilder
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF


# idd is read only once in this test
# if it has already been read from some other test, it will continue with the old reading
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_flattencopy():
    """py.test for flattencopy"""
    tdata = (
        ([1, 2], [1, 2]),  # lst , nlst
        ([1, 2, [3, 4]], [1, 2, 3, 4]),  # lst , nlst
        ([1, 2, [3, [4, 5, 6], 7, 8]], [1, 2, 3, 4, 5, 6, 7, 8]),  # lst , nlst
        ([1, 2, [3, [4, 5, [6, 7], 8], 9]], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        # lst , nlst
    )
    for lst, nlst in tdata:
        result = hvacbuilder.flattencopy(lst)
        assert result == nlst


def test_makeplantloop():
    """pytest for makeplantloop"""
    tdata = (
        (
            "",
            "p_loop",
            ["sb0", ["sb1", "sb2", "sb3"], "sb4"],
            ["db0", ["db1", "db2", "db3"], "db4"],
            """BRANCH, sb0, 0.0, , Pipe:Adiabatic, sb0_pipe, p_loop Supply Inlet,
        sb0_pipe_outlet, Bypass;BRANCH, sb1, 0.0, , Pipe:Adiabatic, sb1_pipe,
        sb1_pipe_inlet, sb1_pipe_outlet, Bypass;BRANCH, sb2, 0.0, ,
        Pipe:Adiabatic, sb2_pipe, sb2_pipe_inlet, sb2_pipe_outlet,
        Bypass;BRANCH, sb3, 0.0, , Pipe:Adiabatic, sb3_pipe, sb3_pipe_inlet,
        sb3_pipe_outlet, Bypass;BRANCH, sb4, 0.0, , Pipe:Adiabatic, sb4_pipe,
        sb4_pipe_inlet, p_loop Supply Outlet, Bypass;BRANCH, db0, 0.0, ,
        Pipe:Adiabatic, db0_pipe, p_loop Demand Inlet, db0_pipe_outlet,
        Bypass;BRANCH, db1, 0.0, , Pipe:Adiabatic, db1_pipe, db1_pipe_inlet,
        db1_pipe_outlet, Bypass;BRANCH, db2, 0.0, , Pipe:Adiabatic, db2_pipe,
        db2_pipe_inlet, db2_pipe_outlet, Bypass;BRANCH, db3, 0.0, ,
        Pipe:Adiabatic, db3_pipe, db3_pipe_inlet, db3_pipe_outlet,
        Bypass;BRANCH, db4, 0.0, , Pipe:Adiabatic, db4_pipe, db4_pipe_inlet,
        p_loop Demand Outlet, Bypass;BRANCHLIST, p_loop Supply Branchs,
        sb0, sb1, sb2, sb3, sb4;BRANCHLIST, p_loop Demand Branchs, db0,
        db1, db2, db3, db4;CONNECTOR:SPLITTER, p_loop_supply_splitter,
        sb0, sb1, sb2, sb3;CONNECTOR:SPLITTER, p_loop_demand_splitter,
        db0, db1, db2, db3;CONNECTOR:MIXER, p_loop_supply_mixer, sb4,
        sb1, sb2, sb3;CONNECTOR:MIXER, p_loop_demand_mixer, db4, db1,
        db2, db3;CONNECTORLIST, p_loop Supply Connectors, Connector:Splitter,
        p_loop_supply_splitter, Connector:Mixer,
        p_loop_supply_mixer;CONNECTORLIST, p_loop Demand Connectors,
        Connector:Splitter, p_loop_demand_splitter, Connector:Mixer,
        p_loop_demand_mixer;PIPE:ADIABATIC, sb0_pipe, p_loop Supply Inlet,
        sb0_pipe_outlet;PIPE:ADIABATIC, sb1_pipe, sb1_pipe_inlet,
        sb1_pipe_outlet;PIPE:ADIABATIC, sb2_pipe, sb2_pipe_inlet,
        sb2_pipe_outlet;PIPE:ADIABATIC, sb3_pipe, sb3_pipe_inlet,
        sb3_pipe_outlet;PIPE:ADIABATIC, sb4_pipe, sb4_pipe_inlet,
        p_loop Supply Outlet;PIPE:ADIABATIC, db0_pipe,
        p_loop Demand Inlet, db0_pipe_outlet;PIPE:ADIABATIC, db1_pipe,
        db1_pipe_inlet, db1_pipe_outlet;PIPE:ADIABATIC, db2_pipe,
        db2_pipe_inlet, db2_pipe_outlet;PIPE:ADIABATIC, db3_pipe,
        db3_pipe_inlet, db3_pipe_outlet;PIPE:ADIABATIC, db4_pipe,
        db4_pipe_inlet, p_loop Demand Outlet;PLANTLOOP, p_loop, Water, , ,
        , , , , 0.0, Autocalculate, p_loop Supply Inlet,
        p_loop Supply Outlet, p_loop Supply Branchs,
        p_loop Supply Connectors, p_loop Demand Inlet, p_loop Demand Outlet,
        p_loop Demand Branchs, p_loop Demand Connectors, Sequential, ,
        SingleSetpoint, None, None;""",
        ),  # blankidf, loopname, sloop, dloop, nidf
    )
    for blankidf, loopname, sloop, dloop, nidf in tdata:
        fhandle = StringIO("")
        idf1 = IDF(fhandle)
        loopname = "p_loop"
        sloop = ["sb0", ["sb1", "sb2", "sb3"], "sb4"]
        dloop = ["db0", ["db1", "db2", "db3"], "db4"]
        hvacbuilder.makeplantloop(idf1, loopname, sloop, dloop)
        idf2 = IDF(StringIO(nidf))
        # print('=' * 15)
        # print(idf1.model)
        # print('-' * 15)
        # print(idf2.model)
        # print('=' * 15)
        assert str(idf1.model) == str(idf2.model)


def test_makecondenserloop():
    """pytest for makecondenserloop"""
    tdata = (
        (
            "",
            "c_loop",
            ["sb0", ["sb1", "sb2", "sb3"], "sb4"],
            ["db0", ["db1", "db2", "db3"], "db4"],
            """BRANCH, sb0, 0.0, , Pipe:Adiabatic, sb0_pipe,
        c_loop Cond_Supply Inlet, sb0_pipe_outlet, Bypass;  BRANCH, sb1, 0.0,
        , Pipe:Adiabatic, sb1_pipe, sb1_pipe_inlet, sb1_pipe_outlet,
        Bypass;  BRANCH, sb2, 0.0, , Pipe:Adiabatic, sb2_pipe,
        sb2_pipe_inlet, sb2_pipe_outlet, Bypass;  BRANCH, sb3, 0.0, ,
        Pipe:Adiabatic, sb3_pipe, sb3_pipe_inlet, sb3_pipe_outlet,
        Bypass;  BRANCH, sb4, 0.0, , Pipe:Adiabatic, sb4_pipe,
        sb4_pipe_inlet, c_loop Cond_Supply Outlet, Bypass;  BRANCH,
        db0, 0.0, , Pipe:Adiabatic, db0_pipe, c_loop Demand Inlet,
        db0_pipe_outlet, Bypass;  BRANCH, db1, 0.0, , Pipe:Adiabatic, db1_pipe,
        db1_pipe_inlet, db1_pipe_outlet, Bypass;  BRANCH, db2, 0.0, ,
        Pipe:Adiabatic, db2_pipe, db2_pipe_inlet, db2_pipe_outlet, Bypass;
        BRANCH, db3, 0.0, , Pipe:Adiabatic, db3_pipe, db3_pipe_inlet,
        db3_pipe_outlet, Bypass;  BRANCH, db4, 0.0, , Pipe:Adiabatic,
        db4_pipe, db4_pipe_inlet, c_loop Demand Outlet, Bypass;
        BRANCHLIST, c_loop Cond_Supply Branchs, sb0, sb1, sb2, sb3, sb4;
        BRANCHLIST, c_loop Condenser Demand Branchs, db0, db1, db2, db3,
        db4;  CONNECTOR:SPLITTER, c_loop_supply_splitter, sb0, sb1,
        sb2, sb3;  CONNECTOR:SPLITTER, c_loop_demand_splitter, db0, db1, db2,
        db3;  CONNECTOR:MIXER, c_loop_supply_mixer, sb4, sb1, sb2, sb3;
        CONNECTOR:MIXER, c_loop_demand_mixer, db4, db1, db2, db3;
        CONNECTORLIST, c_loop Cond_Supply Connectors, Connector:Splitter,
        c_loop_supply_splitter, Connector:Mixer, c_loop_supply_mixer;
        CONNECTORLIST, c_loop Condenser Demand Connectors,
        Connector:Splitter, c_loop_demand_splitter, Connector:Mixer,
        c_loop_demand_mixer;  PIPE:ADIABATIC, sb0_pipe,
        c_loop Cond_Supply Inlet, sb0_pipe_outlet;  PIPE:ADIABATIC,
        sb1_pipe, sb1_pipe_inlet, sb1_pipe_outlet;  PIPE:ADIABATIC, sb2_pipe,
        sb2_pipe_inlet, sb2_pipe_outlet;  PIPE:ADIABATIC, sb3_pipe,
        sb3_pipe_inlet, sb3_pipe_outlet;  PIPE:ADIABATIC, sb4_pipe,
        sb4_pipe_inlet, c_loop Cond_Supply Outlet;  PIPE:ADIABATIC,
        db0_pipe, c_loop Demand Inlet, db0_pipe_outlet;  PIPE:ADIABATIC,
        db1_pipe, db1_pipe_inlet, db1_pipe_outlet;  PIPE:ADIABATIC,
        db2_pipe, db2_pipe_inlet, db2_pipe_outlet;  PIPE:ADIABATIC,
        db3_pipe, db3_pipe_inlet, db3_pipe_outlet;  PIPE:ADIABATIC, db4_pipe,
        db4_pipe_inlet, c_loop Demand Outlet;  CONDENSERLOOP, c_loop, Water, ,
        , , , , , 0.0, Autocalculate, c_loop Cond_Supply Inlet,
        c_loop Cond_Supply Outlet, c_loop Cond_Supply Branchs,
        c_loop Cond_Supply Connectors, c_loop Demand Inlet,
        c_loop Demand Outlet, c_loop Condenser Demand Branchs,
        c_loop Condenser Demand Connectors, Sequential, None;  """,
        ),  # blankidf, loopname, sloop, dloop, nidf
    )
    for blankidf, loopname, sloop, dloop, nidf in tdata:

        fhandle = StringIO("")
        idf1 = IDF(fhandle)
        loopname = "c_loop"
        sloop = ["sb0", ["sb1", "sb2", "sb3"], "sb4"]
        dloop = ["db0", ["db1", "db2", "db3"], "db4"]
        hvacbuilder.makecondenserloop(idf1, loopname, sloop, dloop)
        idf2 = IDF(StringIO(nidf))
        assert str(idf1.model) == str(idf2.model)


def test_getbranchcomponents():
    """py.test for getbranchcomponents"""
    tdata = (
        (
            """BRANCH,
            sb1,
            0.0,
            ,
            PIPE:ADIABATIC,
            np1,
            np1_inlet,
            np1_np2_node,
            ,
            PIPE:ADIABATIC,
            np2,
            np1_np2_node,
            np2_outlet,
            ;
            """,
            True,
            [("PIPE:ADIABATIC", "np1"), ("PIPE:ADIABATIC", "np2")],
        ),  # idftxt, utest, componentlist
        (
            """BRANCH,
            sb1,
            0.0,
            ,
            PIPE:ADIABATIC,
            np1,
            np1_inlet,
            np1_np2_node,
            ,
            PIPE:ADIABATIC,
            np2,
            np1_np2_node,
            np2_outlet,
            ;
            PIPE:ADIABATIC,
            np1,
            np1_inlet,
            np1_np2_node;

            PIPE:ADIABATIC,
            np2,
            np1_np2_node,
            np2_outlet;

            """,
            False,
            [
                ["PIPE:ADIABATIC", "np1", "np1_inlet", "np1_np2_node"],
                ["PIPE:ADIABATIC", "np2", "np1_np2_node", "np2_outlet"],
            ],
        ),
        # idftxt, utest, componentlist
    )
    for idftxt, utest, componentlist in tdata:
        fhandle = StringIO(idftxt)
        idf = IDF(fhandle)
        branch = idf.idfobjects["BRANCH"][0]
        result = hvacbuilder.getbranchcomponents(idf, branch, utest=utest)
        if utest:
            assert result == componentlist
        else:
            lresult = [item.obj for item in result]
            assert lresult == componentlist


def test_renamenodes():
    """py.test for renamenodes"""
    idftxt = """PIPE:ADIABATIC,
         np1,
         np1_inlet,
         np1_outlet;
         !- ['np1_outlet', 'np1_np2_node'];

    BRANCH,
         sb0,
         0.0,
         ,
         Pipe:Adiabatic,
         np1,
         np1_inlet,
         np1_outlet,
         Bypass;
    """
    outtxt = """PIPE:ADIABATIC,
         np1,
         np1_inlet,
         np1_np2_node;
         !- ['np1_outlet', 'np1_np2_node'];

    BRANCH,
         sb0,
         0.0,
         ,
         Pipe:Adiabatic,
         np1,
         np1_inlet,
         np1_np2_node,
         Bypass;
    """
    # !- ['np1_outlet', 'np1_np2_node'];
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    pipe = idf.idfobjects["PIPE:ADIABATIC"][0]
    pipe.Outlet_Node_Name = [
        "np1_outlet",
        "np1_np2_node",
    ]  # this is the first step of the replace
    hvacbuilder.renamenodes(idf, fieldtype="node")
    outidf = IDF(StringIO(outtxt))
    result = idf.idfobjects["PIPE:ADIABATIC"][0].obj
    assert result == outidf.idfobjects["PIPE:ADIABATIC"][0].obj


def test_getfieldnamesendswith():
    """py.test for getfieldnamesendswith"""
    idftxt = """PIPE:ADIABATIC,
        np2,                      !- Name
        np1_np2_node,             !- Inlet Node Name
        np2_outlet;               !- Outlet Node Name

    """
    tdata = (
        ("Inlet_Node_Name", ["Inlet_Node_Name"]),  # endswith, fieldnames
        ("Node_Name", ["Inlet_Node_Name", "Outlet_Node_Name"]),  # endswith, fieldnames
        (
            "Name",
            ["Name", "Inlet_Node_Name", "Outlet_Node_Name"],
        ),  # endswith, fieldnames
    )
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    idfobject = idf.idfobjects["PIPE:ADIABATIC"][0]
    for endswith, fieldnames in tdata:
        result = hvacbuilder.getfieldnamesendswith(idfobject, endswith)
        assert result == fieldnames


def test_getnodefieldname():
    """py.test for getnodefieldname"""
    tdata = (
        ("PIPE:ADIABATIC", "pipe1", "Inlet_Node_Name", "", "Inlet_Node_Name"),
        # objtype, objname, endswith, fluid, nodefieldname
        (
            "CHILLER:ELECTRIC",
            "pipe1",
            "Inlet_Node_Name",
            "",
            "Chilled_Water_Inlet_Node_Name",
        ),
        # objtype, objname, endswith, fluid, nodefieldname
        (
            "COIL:COOLING:WATER",
            "pipe1",
            "Inlet_Node_Name",
            "Water",
            "Water_Inlet_Node_Name",
        ),
        # objtype, objname, endswith, fluid, nodefieldname
        (
            "COIL:COOLING:WATER",
            "pipe1",
            "Inlet_Node_Name",
            "Air",
            "Air_Inlet_Node_Name",
        ),
        # objtype, objname, endswith, fluid, nodefieldname
        (
            "COIL:COOLING:WATER",
            "pipe1",
            "Outlet_Node_Name",
            "Air",
            "Air_Outlet_Node_Name",
        ),
        # objtype, objname, endswith, fluid, nodefieldname
    )
    for objtype, objname, endswith, fluid, nodefieldname in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        idfobject = idf.newidfobject(objtype, Name=objname)
        result = hvacbuilder.getnodefieldname(idfobject, endswith, fluid)
        assert result == nodefieldname


def test_connectcomponents():
    """py.test for connectcomponents"""
    fhandle = StringIO("")
    idf = IDF(fhandle)

    tdata = (
        (
            [
                (idf.newidfobject("PIPE:ADIABATIC", Name="pipe1"), None),
                (idf.newidfobject("PIPE:ADIABATIC", Name="pipe2"), None),
            ],
            ["pipe1_Inlet_Node_Name", ["pipe2_Inlet_Node_Name", "pipe1_pipe2_node"]],
            [["pipe1_Outlet_Node_Name", "pipe1_pipe2_node"], "pipe2_Outlet_Node_Name"],
            "",
        ),
        # components_thisnodes, inlets, outlets, fluid
        (
            [
                (idf.newidfobject("Coil:Cooling:Water", Name="pipe1"), "Water_"),
                (idf.newidfobject("Coil:Cooling:Water", Name="pipe2"), "Water_"),
            ],
            [
                "pipe1_Water_Inlet_Node_Name",
                "",
                "pipe2_Water_Inlet_Node_Name",
                ["", "pipe1_pipe2_node"],
            ],
            [
                ["pipe1_Water_Outlet_Node_Name", "pipe1_pipe2_node"],
                "",
                "pipe2_Water_Outlet_Node_Name",
                "",
            ],
            "Air",
        ),
        # components_thisnodes, inlets, outlets, fluid
        (
            [
                (idf.newidfobject("PIPE:ADIABATIC", Name="pipe1"), None),
                (idf.newidfobject("Coil:Cooling:Water", Name="pipe2"), "Water_"),
            ],
            [
                "pipe1_Inlet_Node_Name",
                "pipe2_Water_Inlet_Node_Name",
                ["pipe2_Air_Inlet_Node_Name", "pipe1_pipe2_node"],
            ],
            [
                ["pipe1_Outlet_Node_Name", "pipe1_pipe2_node"],
                "pipe2_Water_Outlet_Node_Name",
                "",
            ],
            "Air",
        ),
        # components_thisnodes, inlets, outlets, fluid
    )
    for components_thisnodes, inlets, outlets, fluid in tdata:
        # init the nodes in the new components
        for component, thisnode in components_thisnodes:
            hvacbuilder.initinletoutlet(idf, component, thisnode)
        hvacbuilder.connectcomponents(idf, components_thisnodes, fluid)
        inresult = []
        for component, thisnode in components_thisnodes:
            fldnames = hvacbuilder.getfieldnamesendswith(component, "Inlet_Node_Name")
            for name in fldnames:
                inresult.append(component[name])
        assert inresult == inresult
        outresult = []
        for component, thisnode in components_thisnodes:
            fldnames = hvacbuilder.getfieldnamesendswith(component, "Outlet_Node_Name")
            for name in fldnames:
                outresult.append(component[name])
        assert outresult == outlets


def test_initinletoutlet():
    """py.test for initinletoutlet"""
    tdata = (
        (
            "PIPE:ADIABATIC",
            "apipe",
            None,
            True,
            ["apipe_Inlet_Node_Name"],
            ["apipe_Outlet_Node_Name"],
        ),
        # idfobjectkey, idfobjname, thisnode, force, inlets, outlets
        ("PIPE:ADIABATIC", "apipe", None, False, ["Gumby"], ["apipe_Outlet_Node_Name"]),
        # idfobjectkey, idfobjname, thisnode, force, inlets, outlets
        (
            "Coil:Cooling:Water",
            "acoil",
            "Water_",
            True,
            ["acoil_Water_Inlet_Node_Name", ""],
            ["acoil_Water_Outlet_Node_Name", ""],
        ),
        # idfobjectkey, idfobjname, thisnode, force, inlets, outlets
    )
    fhandle = StringIO("")
    idf = IDF(fhandle)
    for idfobjectkey, idfobjname, thisnode, force, inlets, outlets in tdata:
        idfobject = idf.newidfobject(idfobjectkey, Name=idfobjname)
        inodefields = hvacbuilder.getfieldnamesendswith(idfobject, "Inlet_Node_Name")
        idfobject[inodefields[0]] = "Gumby"
        hvacbuilder.initinletoutlet(idf, idfobject, thisnode, force=force)
        inodefields = hvacbuilder.getfieldnamesendswith(idfobject, "Inlet_Node_Name")
        for nodefield, inlet in zip(inodefields, inlets):
            result = idfobject[nodefield]
            assert result == inlet
        onodefields = hvacbuilder.getfieldnamesendswith(idfobject, "Outlet_Node_Name")
        for nodefield, outlet in zip(onodefields, outlets):
            result = idfobject[nodefield]
            assert result == outlet


def test_componentsintobranch():
    """py.test for componentsintobranch"""
    tdata = (
        (
            """BRANCH,
             sb0,
             0.0,
             ,
             Pipe:Adiabatic,
             sb0_pipe,
             p_loop Supply Inlet,
             sb0_pipe_outlet,
             Bypass;
             """,
            [("PIPE:ADIABATIC", "pipe1", None), ("PIPE:ADIABATIC", "pipe2", None)],
            "",
            [
                "PIPE:ADIABATIC",
                "pipe1",
                "pipe1_Inlet_Node_Name",
                "pipe1_Outlet_Node_Name",
                "",
                "PIPE:ADIABATIC",
                "pipe2",
                "pipe2_Inlet_Node_Name",
                "pipe2_Outlet_Node_Name",
                "",
            ],
        ),
        # idftxt, complst, fluid, branchcomps
        (
            """BRANCH,
            sb0,
            0.0,
            ,
            Pipe:Adiabatic,
            sb0_pipe,
            p_loop Supply Inlet,
            sb0_pipe_outlet,
            Bypass;
            """,
            [
                ("PIPE:ADIABATIC", "pipe1", None),
                ("CHILLER:ELECTRIC", "chiller", "Chilled_Water_"),
            ],
            "",
            [
                "PIPE:ADIABATIC",
                "pipe1",
                "pipe1_Inlet_Node_Name",
                "pipe1_Outlet_Node_Name",
                "",
                "CHILLER:ELECTRIC",
                "chiller",
                "chiller_Chilled_Water_Inlet_Node_Name",
                "chiller_Chilled_Water_Outlet_Node_Name",
                "",
            ],
        ),
        # idftxt, complst, fluid, branchcomps
    )
    for ii, (idftxt, complst, fluid, branchcomps) in enumerate(tdata):
        fhandle = StringIO(idftxt)
        idf = IDF(fhandle)
        components_thisnodes = [
            (idf.newidfobject(key, Name=nm), thisnode) for key, nm, thisnode in complst
        ]
        fnc = hvacbuilder.initinletoutlet
        components_thisnodes = [
            (fnc(idf, cp, thisnode), thisnode) for cp, thisnode in components_thisnodes
        ]
        branch = idf.idfobjects["BRANCH"][0]
        branch = hvacbuilder.componentsintobranch(
            idf, branch, components_thisnodes, fluid
        )
        assert branch.obj[4:] == branchcomps


def test_replacebranch():
    """py.test for replacebranch"""
    tdata = (
        (
            "p_loop",
            ["sb0", ["sb1", "sb2", "sb3"], "sb4"],
            ["db0", ["db1", "db2", "db3"], "db4"],
            "sb0",
            [
                ("Chiller:Electric", "Central_Chiller", "Chilled_Water_"),
                ("PIPE:ADIABATIC", "np1", None),
                ("PIPE:ADIABATIC", "np2", None),
            ],
            "Water",
            [
                "BRANCH",
                "sb0",
                0.0,
                "",
                "CHILLER:ELECTRIC",
                "Central_Chiller",
                "p_loop Supply Inlet",
                "Central_Chiller_np1_node",
                "",
                "PIPE:ADIABATIC",
                "np1",
                "Central_Chiller_np1_node",
                "np1_np2_node",
                "",
                "PIPE:ADIABATIC",
                "np2",
                "np1_np2_node",
                "np2_Outlet_Node_Name",
                "",
            ],
        ),  # loopname, sloop, dloop, branchname, componenttuple, fluid, outbranch
    )
    for (loopname, sloop, dloop, branchname, componenttuple, fluid, outbranch) in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        loop = hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
        components_thisnodes = [
            (idf.newidfobject(key, Name=nm), thisnode)
            for key, nm, thisnode in componenttuple
        ]
        branch = idf.getobject("BRANCH", branchname)
        newbr = hvacbuilder.replacebranch(
            idf, loop, branch, components_thisnodes, fluid=fluid
        )
        assert newbr.obj == outbranch


def test_makepipecomponent():
    """py.test for makepipecomponent"""
    tdata = (
        (
            "apipe",
            ["PIPE:ADIABATIC", "apipe", "apipe_inlet", "apipe_outlet"],
        ),  # pname, pipe_obj
        (
            "bpipe",
            ["PIPE:ADIABATIC", "bpipe", "bpipe_inlet", "bpipe_outlet"],
        ),  # pname, pipe_obj
    )
    for pname, pipe_obj in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = hvacbuilder.makepipecomponent(idf, pname)
        assert result.obj == pipe_obj


def test_makeductcomponent():
    """py.test for makeductcomponent"""
    tdata = (
        ("aduct", ["DUCT", "aduct", "aduct_inlet", "aduct_outlet"]),  # dname, duct_obj
    )
    for dname, duct_obj in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = hvacbuilder.makeductcomponent(idf, dname)
        assert result.obj == duct_obj


def test_makepipebranch():
    """py.test for makepipebranch"""
    tdata = (
        (
            "p_branch",
            [
                "BRANCH",
                "p_branch",
                0.0,
                "",
                "Pipe:Adiabatic",
                "p_branch_pipe",
                "p_branch_pipe_inlet",
                "p_branch_pipe_outlet",
                "Bypass",
            ],
            [
                "PIPE:ADIABATIC",
                "p_branch_pipe",
                "p_branch_pipe_inlet",
                "p_branch_pipe_outlet",
            ],
        ),  # pb_name, branch_obj, pipe_obj
    )
    for pb_name, branch_obj, pipe_obj in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = hvacbuilder.makepipebranch(idf, pb_name)
        assert result.obj == branch_obj
        thepipe = idf.getobject("PIPE:ADIABATIC", result.Component_1_Name)
        assert thepipe.obj == pipe_obj


def test_makeductbranch():
    """py.test for makeductbranch"""
    tdata = (
        (
            "d_branch",
            [
                "BRANCH",
                "d_branch",
                0.0,
                "",
                "duct",
                "d_branch_duct",
                "d_branch_duct_inlet",
                "d_branch_duct_outlet",
                "Bypass",
            ],
            ["DUCT", "d_branch_duct", "d_branch_duct_inlet", "d_branch_duct_outlet"],
        ),  # db_name, branch_obj, duct_obj
    )
    for db_name, branch_obj, duct_obj in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = hvacbuilder.makeductbranch(idf, db_name)
        assert result.obj == branch_obj
        theduct = idf.getobject("DUCT", result.Component_1_Name)
        assert theduct.obj == duct_obj


def test_clean_listofcomponents():
    """py.test for _clean_listofcomponents"""
    data = (
        ([1, 2], [(1, None), (2, None)]),  # lst, clst
        ([(1, None), 2], [(1, None), (2, None)]),  # lst, clst
        ([(1, "stuff"), 2], [(1, "stuff"), (2, None)]),  # lst, clst
    )
    for lst, clst in data:
        result = hvacbuilder._clean_listofcomponents(lst)
        assert result == clst


def test_clean_listofcomponents_tuples():
    """py.test for _clean_listofcomponents_tuples"""
    data = (
        ([(1, 2), (2, 3)], [(1, 2, None), (2, 3, None)]),  # lst, clst
        ([(1, 2, None), (2, 3)], [(1, 2, None), (2, 3, None)]),  # lst, clst
        ([(1, 2, "stuff"), (2, 3)], [(1, 2, "stuff"), (2, 3, None)]),  # lst, clst
    )
    for lst, clst in data:
        result = hvacbuilder._clean_listofcomponents_tuples(lst)
        assert result == clst
