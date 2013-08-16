# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

idfsnippet = """
Building,
  Building,                !- Name
  30.,                     !- North Axis {deg}
  City,                    !- Terrain
  0.04,                    !- Loads Convergence Tolerance Value
  0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
  FullExterior,            !- Solar Distribution
  25,                      !- Maximum Number of Warmup Days
  6;                       !- Minimum Number of Warmup Days

Building,
  Building,                !- Name
  30,                       !- North Axis {deg}
  City;                    !- Terrain

Building,
  BuildinG,                !- Name
  30.001,                       !- North Axis {deg}
  CitY;                    !- Terrain

Building,
  Building,                !- Name
  30.,                     !- North Axis {deg}
  City,                    !- Terrain
  0.04,                    !- Loads Convergence Tolerance Value
  0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
  FullExterior,            !- Solar Distribution
  25,                      !- Maximum Number of Warmup Days
  7;                       !- Minimum Number of Warmup Days


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

BuildingSurface:Detailed,
    WALL-1PF,                !- Name
    WALL,                    !- Surface Type
    WALL-1,                  !- Construction Name
    PLENUM-1,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.50000,                 !- View Factor to Ground
    4,                       !- Number of Vertices
    0.0,0.0,3.0,  !- X,Y,Z ==> Vertex 1 {m}
    0.0,0.0,2.4,  !- X,Y,Z ==> Vertex 2 {m}
    30.5,0.0,2.4,  !- X,Y,Z ==> Vertex 3 {m}
    30.5,0.0,3.0;  !- X,Y,Z ==> Vertex 4 {m}

"""

