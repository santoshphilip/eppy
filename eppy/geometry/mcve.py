from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from io import StringIO


iddsnippet = iddcurrent.iddtxt
iddfhandle = StringIO(iddcurrent.iddtxt)
IDF.setiddname(iddfhandle)

idftxt = """

Version,                  
    8.5;                      !- Version Identifier

Building,                 
    Building 1,               !- Name
    ,                         !- North Axis
    ,                         !- Terrain
    ,                         !- Loads Convergence Tolerance Value
    ,                         !- Temperature Convergence Tolerance Value
    ,                         !- Solar Distribution
    ,                         !- Maximum Number of Warmup Days
    ;                         !- Minimum Number of Warmup Days

Zone,                     
    Thermal Zone 1,           !- Name
    -0.0,                     !- Direction of Relative North
    3.41258124196863,         !- X Origin
    0.821279819391803,        !- Y Origin
    0.7279,                   !- Z Origin
    ,                         !- Type
    ,                         !- Multiplier
    ,                         !- Ceiling Height
    ,                         !- Volume
    ,                         !- Floor Area
    ,                         !- Zone Inside Convection Algorithm
    ;                         !- Zone Outside Convection Algorithm

Zone,                     
    Thermal Zone 2,           !- Name
    -0.0,                     !- Direction of Relative North
    3.41258124196863,         !- X Origin
    0.821279819391803,        !- Y Origin
    0.0,                      !- Z Origin
    ,                         !- Type
    ,                         !- Multiplier
    ,                         !- Ceiling Height
    ,                         !- Volume
    ,                         !- Floor Area
    ,                         !- Zone Inside Convection Algorithm
    ;                         !- Zone Outside Convection Algorithm

BuildingSurface:Detailed, 
    z1 Floor 0001,            !- Name
    Floor,                    !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 1,           !- Zone Name
    Ground,                   !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    NoSun,                    !- Sun Exposure
    NoWind,                   !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -0.259,                   !- Vertex 1 Xcoordinate
    2.46,                     !- Vertex 1 Ycoordinate
    0.0,                      !- Vertex 1 Zcoordinate
    -0.259,                   !- Vertex 2 Xcoordinate
    0.4,                      !- Vertex 2 Ycoordinate
    0.0,                      !- Vertex 2 Zcoordinate
    -1.68,                    !- Vertex 3 Xcoordinate
    0.4,                      !- Vertex 3 Ycoordinate
    0.0,                      !- Vertex 3 Zcoordinate
    -1.68,                    !- Vertex 4 Xcoordinate
    2.46,                     !- Vertex 4 Ycoordinate
    0.0;                      !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z1 Wall 0001,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 1,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -0.259,                   !- Vertex 1 Xcoordinate
    2.46,                     !- Vertex 1 Ycoordinate
    0.7279,                   !- Vertex 1 Zcoordinate
    -0.259,                   !- Vertex 2 Xcoordinate
    2.46,                     !- Vertex 2 Ycoordinate
    0.0,                      !- Vertex 2 Zcoordinate
    -1.68,                    !- Vertex 3 Xcoordinate
    2.46,                     !- Vertex 3 Ycoordinate
    0.0,                      !- Vertex 3 Zcoordinate
    -1.68,                    !- Vertex 4 Xcoordinate
    2.46,                     !- Vertex 4 Ycoordinate
    0.7279;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z1 Wall 0002,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 1,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -0.259,                   !- Vertex 1 Xcoordinate
    0.4,                      !- Vertex 1 Ycoordinate
    0.7279,                   !- Vertex 1 Zcoordinate
    -0.259,                   !- Vertex 2 Xcoordinate
    0.4,                      !- Vertex 2 Ycoordinate
    0.0,                      !- Vertex 2 Zcoordinate
    -0.259,                   !- Vertex 3 Xcoordinate
    2.46,                     !- Vertex 3 Ycoordinate
    0.0,                      !- Vertex 3 Zcoordinate
    -0.259,                   !- Vertex 4 Xcoordinate
    2.46,                     !- Vertex 4 Ycoordinate
    0.7279;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z1 Wall 0003,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 1,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -1.68,                    !- Vertex 1 Xcoordinate
    0.4,                      !- Vertex 1 Ycoordinate
    0.7279,                   !- Vertex 1 Zcoordinate
    -1.68,                    !- Vertex 2 Xcoordinate
    0.4,                      !- Vertex 2 Ycoordinate
    0.0,                      !- Vertex 2 Zcoordinate
    -0.259,                   !- Vertex 3 Xcoordinate
    0.4,                      !- Vertex 3 Ycoordinate
    0.0,                      !- Vertex 3 Zcoordinate
    -0.259,                   !- Vertex 4 Xcoordinate
    0.4,                      !- Vertex 4 Ycoordinate
    0.7279;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z1 Wall 0004,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 1,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -1.68,                    !- Vertex 1 Xcoordinate
    2.46,                     !- Vertex 1 Ycoordinate
    0.7279,                   !- Vertex 1 Zcoordinate
    -1.68,                    !- Vertex 2 Xcoordinate
    2.46,                     !- Vertex 2 Ycoordinate
    0.0,                      !- Vertex 2 Zcoordinate
    -1.68,                    !- Vertex 3 Xcoordinate
    0.4,                      !- Vertex 3 Ycoordinate
    0.0,                      !- Vertex 3 Zcoordinate
    -1.68,                    !- Vertex 4 Xcoordinate
    0.4,                      !- Vertex 4 Ycoordinate
    0.7279;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z1 Roof 0001,             !- Name
    Roof,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 1,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -0.259,                   !- Vertex 1 Xcoordinate
    0.4,                      !- Vertex 1 Ycoordinate
    0.7279,                   !- Vertex 1 Zcoordinate
    -0.259,                   !- Vertex 2 Xcoordinate
    2.46,                     !- Vertex 2 Ycoordinate
    0.7279,                   !- Vertex 2 Zcoordinate
    -1.68,                    !- Vertex 3 Xcoordinate
    2.46,                     !- Vertex 3 Ycoordinate
    0.7279,                   !- Vertex 3 Zcoordinate
    -1.68,                    !- Vertex 4 Xcoordinate
    0.4,                      !- Vertex 4 Ycoordinate
    0.7279;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z2 Floor 0001,            !- Name
    Floor,                    !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 2,           !- Zone Name
    Ground,                   !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    NoSun,                    !- Sun Exposure
    NoWind,                   !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    0.0,                      !- Vertex 1 Xcoordinate
    2.9,                      !- Vertex 1 Ycoordinate
    0.7279,                      !- Vertex 1 Zcoordinate
    0.0,                      !- Vertex 2 Xcoordinate
    0.0,                      !- Vertex 2 Ycoordinate
    0.7279,                      !- Vertex 2 Zcoordinate
    -2.14,                    !- Vertex 3 Xcoordinate
    0.0,                      !- Vertex 3 Ycoordinate
    0.7279,                      !- Vertex 3 Zcoordinate
    -2.14,                    !- Vertex 4 Xcoordinate
    2.9,                      !- Vertex 4 Ycoordinate
    0.7279;                      !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z2 Wall 0001,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 2,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -2.14,                    !- Vertex 1 Xcoordinate
    0.0,                      !- Vertex 1 Ycoordinate
    1.458,                   !- Vertex 1 Zcoordinate
    -2.14,                    !- Vertex 2 Xcoordinate
    0.0,                      !- Vertex 2 Ycoordinate
    0.7279,                      !- Vertex 2 Zcoordinate
    0.0,                      !- Vertex 3 Xcoordinate
    0.0,                      !- Vertex 3 Ycoordinate
    0.7279,                      !- Vertex 3 Zcoordinate
    0.0,                      !- Vertex 4 Xcoordinate
    0.0,                      !- Vertex 4 Ycoordinate
    1.458;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z2 Wall 0002,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 2,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    -2.14,                    !- Vertex 1 Xcoordinate
    2.9,                      !- Vertex 1 Ycoordinate
    1.458,                   !- Vertex 1 Zcoordinate
    -2.14,                    !- Vertex 2 Xcoordinate
    2.9,                      !- Vertex 2 Ycoordinate
    0.7279,                      !- Vertex 2 Zcoordinate
    -2.14,                    !- Vertex 3 Xcoordinate
    0.0,                      !- Vertex 3 Ycoordinate
    0.7279,                      !- Vertex 3 Zcoordinate
    -2.14,                    !- Vertex 4 Xcoordinate
    0.0,                      !- Vertex 4 Ycoordinate
    1.458;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z2 Wall 0003,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 2,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    0.0,                      !- Vertex 1 Xcoordinate
    2.9,                      !- Vertex 1 Ycoordinate
    1.458,                   !- Vertex 1 Zcoordinate
    0.0,                      !- Vertex 2 Xcoordinate
    2.9,                      !- Vertex 2 Ycoordinate
    0.7279,                      !- Vertex 2 Zcoordinate
    -2.14,                    !- Vertex 3 Xcoordinate
    2.9,                      !- Vertex 3 Ycoordinate
    0.7279,                      !- Vertex 3 Zcoordinate
    -2.14,                    !- Vertex 4 Xcoordinate
    2.9,                      !- Vertex 4 Ycoordinate
    1.458;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z2 Wall 0004,             !- Name
    Wall,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 2,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    0.0,                      !- Vertex 1 Xcoordinate
    0.0,                      !- Vertex 1 Ycoordinate
    1.458,                   !- Vertex 1 Zcoordinate
    0.0,                      !- Vertex 2 Xcoordinate
    0.0,                      !- Vertex 2 Ycoordinate
    0.7279,                      !- Vertex 2 Zcoordinate
    0.0,                      !- Vertex 3 Xcoordinate
    2.9,                      !- Vertex 3 Ycoordinate
    0.7279,                      !- Vertex 3 Zcoordinate
    0.0,                      !- Vertex 4 Xcoordinate
    2.9,                      !- Vertex 4 Ycoordinate
    1.458;                   !- Vertex 4 Zcoordinate

BuildingSurface:Detailed, 
    z2 Roof 0001,             !- Name
    Roof,                     !- Surface Type
    ,                         !- Construction Name
    Thermal Zone 2,           !- Zone Name
    Outdoors,                 !- Outside Boundary Condition
    ,                         !- Outside Boundary Condition Object
    SunExposed,               !- Sun Exposure
    WindExposed,              !- Wind Exposure
    ,                         !- View Factor to Ground
    ,                         !- Number of Vertices
    0.0,                      !- Vertex 1 Xcoordinate
    0.0,                      !- Vertex 1 Ycoordinate
    1.458,                   !- Vertex 1 Zcoordinate
    0.0,                      !- Vertex 2 Xcoordinate
    2.9,                      !- Vertex 2 Ycoordinate
    1.458,                   !- Vertex 2 Zcoordinate
    -2.14,                    !- Vertex 3 Xcoordinate
    2.9,                      !- Vertex 3 Ycoordinate
    1.458,                   !- Vertex 3 Zcoordinate
    -2.14,                    !- Vertex 4 Xcoordinate
    0.0,                      !- Vertex 4 Ycoordinate
    1.458;                   !- Vertex 4 Zcoordinate

"""
idf = IDF()
idf.initreadtxt(idftxt)

idf.outputtype = "compressed"
idf.printidf()
