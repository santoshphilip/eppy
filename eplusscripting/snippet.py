idfsnippet = """
Zone,
  PLENUM-1,                !- Name
  0,                       !- Direction of Relative North {deg}
  0,                       !- X Origin {m}
  0,                       !- Y Origin {m}
  0,                       !- Z Origin {m}
  1,                       !- Type
  1,                       !- Multiplier
  0.609600067,             !- Ceiling Height {m}
  283.2;                   !- Volume {m3}

Zone,
  SPACE1-1,                !- Name
  0,                       !- Direction of Relative North {deg}
  0,                       !- X Origin {m}
  0,                       !- Y Origin {m}
  0,                       !- Z Origin {m}
  1,                       !- Type
  1,                       !- Multiplier
  2.438400269,             !- Ceiling Height {m}
  239.247360229;           !- Volume {m3}

Zone,
  SPACE2-1,                !- Name
  0,                       !- Direction of Relative North {deg}
  0,                       !- X Origin {m}
  0,                       !- Y Origin {m}
  0,                       !- Z Origin {m}
  1,                       !- Type
  1,                       !- Multiplier
  2.438400269,             !- Ceiling Height {m}
  103.311355591;           !- Volume {m3}

Zone,
  SPACE3-1,                !- Name
  0,                       !- Direction of Relative North {deg}
  0,                       !- X Origin {m}
  0,                       !- Y Origin {m}
  0,                       !- Z Origin {m}
  1,                       !- Type
  1,                       !- Multiplier
  2.438400269,             !- Ceiling Height {m}
  239.247360229;           !- Volume {m3}

Zone,
  SPACE4-1,                !- Name
  0,                       !- Direction of Relative North {deg}
  0,                       !- X Origin {m}
  0,                       !- Y Origin {m}
  0,                       !- Z Origin {m}
  1,                       !- Type
  1,                       !- Multiplier
  2.438400269,             !- Ceiling Height {m}
  103.311355591;           !- Volume {m3}

Zone,
  SPACE5-1,                !- Name
  0,                       !- Direction of Relative North {deg}
  0,                       !- X Origin {m}
  0,                       !- Y Origin {m}
  0,                       !- Z Origin {m}
  1,                       !- Type
  1,                       !- Multiplier
  2.438400269,             !- Ceiling Height {m}
  447.682556152;           !- Volume {m3}

Zone,
  Sup-PLENUM-1,            !- Name
  0,                       !- Direction of Relative North {deg}
  0,                       !- X Origin {m}
  0,                       !- Y Origin {m}
  0,                       !- Z Origin {m}
  1,                       !- Type
  1,                       !- Multiplier
  0.45,                    !- Ceiling Height {m}
  208.6;                   !- Volume {m3}
"""

iddsnippet = """Zone,
  \\format vertices
  A1 , \\field Name
       \\required-field
       \\type alpha
       \\reference ZoneNames
       \\reference OutFaceEnvNames
       \\reference ZoneAndZoneListNames
       \\reference AirflowNetworkNodeAndZoneNames
  N1 , \\field Direction of Relative North
       \\units deg
       \\type real
       \\default 0
  N2 , \\field X Origin
       \\units m
       \\type real
       \\default 0
  N3 , \\field Y Origin
       \\units m
       \\type real
       \\default 0
  N4 , \\field Z Origin
       \\units m
       \\type real
       \\default 0
  N5 , \\field Type
       \\type integer
       \\maximum 1
       \\minimum 1
       \\default 1
  N6 , \\field Multiplier
       \\type integer
       \\minimum 1
       \\default 1
  N7 , \\field Ceiling Height
       \\note If this field is 0.0, negative or autocalculate, then the average height
       \\note of the zone is automatically calculated and used in subsequent calculations.
       \\note If this field is positive, then the number entered here will be used.
       \\note Note that the Zone Ceiling Height is the distance from the Floor to
       \\note the Ceiling in the Zone, not an absolute height from the ground.
       \\units m
       \\type real
       \\autocalculatable
       \\default autocalculate
  N8 , \\field Volume
       \\note If this field is 0.0, negative or autocalculate, then the volume of the zone
       \\note is automatically calculated and used in subsequent calculations.
       \\note If this field is positive, then the number entered here will be used.
       \\units m3
       \\type real
       \\autocalculatable
       \\default autocalculate
  N9 , \\field Floor Area
       \\note If this field is 0.0, negative or autocalculate, then the floor area of the zone
       \\note is automatically calculated and used in subsequent calculations.
       \\note If this field is positive, then the number entered here will be used.
       \\units m2
       \\type real
       \\autocalculatable
       \\default autocalculate
  A2 , \\field Zone Inside Convection Algorithm
       \\type choice
       \\key Simple
       \\key TARP
       \\key CeilingDiffuser
       \\key AdaptiveConvectionAlgorithm
       \\key TrombeWall
       \\note Will default to same value as SurfaceConvectionAlgorithm:Inside object
       \\note setting this field overrides the default SurfaceConvectionAlgorithm:Inside for this zone
       \\note Simple = constant natural convection (ASHRAE)
       \\note TARP = variable natural convection based on temperature difference (ASHRAE)
       \\note CeilingDiffuser = ACH based forced and mixed convection correlations
       \\note  for ceiling diffuser configuration with simple natural convection limit
       \\note AdaptiveConvectionAlgorithm = dynamic selection of convection models based on conditions
       \\note TrombeWall = variable natural convection in an enclosed rectangular cavity
  A3,  \\field Zone Outside Convection Algorithm
       \\note Will default to same value as SurfaceConvectionAlgorithm:Outside object
       \\note setting this field overrides the default SurfaceConvectionAlgorithm:Outside for this zone
       \\type choice
       \\key SimpleCombined
       \\key TARP
       \\key DOE-2
       \\key MoWiTT
       \\key AdaptiveConvectionAlgorithm
       \\note SimpleCombined = Combined radiation and convection coefficient using simple ASHRAE model
       \\note TARP = correlation from models developed by ASHRAE, Walton, and Sparrow et. al.
       \\note MoWiTT = correlation from measurements by Klems and Yazdanian for smooth surfaces
       \\note DOE-2 = correlation from measurements by Klems and Yazdanian for rough surfaces
       \\note AdaptiveConvectionAlgorithm = dynamic selection of correlations based on conditions
  A4;  \\field Part of Total Floor Area
       \\type choice
       \\key Yes
       \\key No
       \\default Yes

"""
# import os
# # def test_makefile(tmpdir):
# #     """docstring for test_makefile"""
# #     p = tmpdir.mkdir("sub").join("hello.txt")
# #     p.write(idfsnippet)
# #     print tmpdir
# #     print tmpdir.listdir()
# #     assert 0
# 
# from tempdir import TempDir
# with TempDir() as d:
#     fname = os.path.join(d.name, "piece.idf")
#     open(fname, 'w').write(idfsnippet)
#     ntxt = open(fname, 'r').read()
# print ntxt[:100]
    