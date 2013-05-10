"""py.test for hvacbuilder"""
import sys
import os
sys.path.append('../')
import hvacbuilder
from modeleditor import IDF
import random
from StringIO import StringIO

iddtxt = """Branch,
        \\extensible:5 Just duplicate last 5 fields and comments (changing numbering, please)
        \\memo List components on the branch in simulation and connection order
        \\memo Note: this should NOT include splitters or mixers which define
        \\memo endpoints of branches
   A1,  \\field Name
        \\required-field
        \\reference Branches
   N1, \\field Maximum Flow Rate
        \\default 0
        \\units m3/s
        \\minimum 0
        \\autosizable
   A2, \\field Pressure Drop Curve Name
        \\type object-list
        \\object-list AllCurves
        \\note Optional field to include this branch in plant pressure drop calculations
        \\note This field is only relevant for branches in PlantLoops and CondenserLoops
        \\note Air loops do not account for pressure drop using this field
   A3, \\field Component 1 Object Type
        \\begin-extensible
        \\required-field
   A4, \\field Component 1 Name
        \\required-field
   A5, \\field Component 1 Inlet Node Name
        \\required-field
   A6, \\field Component 1 Outlet Node Name
        \\required-field
   A7, \\field Component 1 Branch Control Type
        \\required-field
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A8, \\field Component 2 Object Type
   A9, \\field Component 2 Name
   A10,\\field Component 2 Inlet Node Name
   A11, \\field Component 2 Outlet Node Name
   A12, \\field Component 2 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A13, \\field Component 3 Object Type
   A14, \\field Component 3 Name
   A15, \\field Component 3 Inlet Node Name
   A16, \\field Component 3 Outlet Node Name
   A17, \\field Component 3 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A18, \\field Component 4 Object Type
   A19, \\field Component 4 Name
   A20, \\field Component 4 Inlet Node Name
   A21, \\field Component 4 Outlet Node Name
   A22, \\field Component 4 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A23, \\field Component 5 Object Type
   A24, \\field Component 5 Name
   A25, \\field Component 5 Inlet Node Name
   A26, \\field Component 5 Outlet Node Name
   A27, \\field Component 5 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A28, \\field Component 6 Object Type
   A29, \\field Component 6 Name
   A30, \\field Component 6 Inlet Node Name
   A31, \\field Component 6 Outlet Node Name
   A32, \\field Component 6 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A33, \\field Component 7 Object Type
   A34, \\field Component 7 Name
   A35, \\field Component 7 Inlet Node Name
   A36, \\field Component 7 Outlet Node Name
   A37, \\field Component 7 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A38, \\field Component 8 Object Type
   A39, \\field Component 8 Name
   A40, \\field Component 8 Inlet Node Name
   A41, \\field Component 8 Outlet Node Name
   A42, \\field Component 8 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A43, \\field Component 9 Object Type
   A44, \\field Component 9 Name
   A45, \\field Component 9 Inlet Node Name
   A46, \\field Component 9 Outlet Node Name
   A47, \\field Component 9 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A48, \\field Component 10 Object Type
   A49, \\field Component 10 Name
   A50, \\field Component 10 Inlet Node Name
   A51, \\field Component 10 Outlet Node Name
   A52, \\field Component 10 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass
   A53, \\field Component 11 Object Type
   A54, \\field Component 11 Name
   A55, \\field Component 11 Inlet Node Name
   A56, \\field Component 11 Outlet Node Name
   A57; \\field Component 11 Branch Control Type
       \\type choice
       \\key Active
       \\key Passive
       \\key SeriesActive
       \\key Bypass
       \\note for ACTIVE, Component tries to set branch flow and turns off branch if the component is off
       \\note for PASSIVE, Component does not try to set branch flow
       \\note for SERIESACTIVE, component is active but does not turn off branch when the component is off
       \\note for BYPASS,  Component designates a loop bypass

BranchList,
 \\extensible:1 Just duplicate last field and comments (changing numbering, please)
 \\memo Branches MUST be listed in Flow order: Inlet branch, then parallel branches, then Outlet branch.
 \\memo Branches are simulated in the order listed.  Branch names cannot be duplicated within a single branch list.
   A1,  \\field Name
       \\required-field
       \\reference BranchLists
   A2, \\field Branch 1 Name
       \\begin-extensible
       \\required-field
       \\type object-list
       \\object-list Branches
   A3, \\field Branch 2 Name
       \\type object-list
       \\object-list Branches
   A4, \\field Branch 3 Name
       \\type object-list
       \\object-list Branches
   A5, \\field Branch 4 Name
       \\type object-list
       \\object-list Branches
   A6, \\field Branch 5 Name
       \\type object-list
       \\object-list Branches
   A7, \\field Branch 6 Name
       \\type object-list
       \\object-list Branches
   A8, \\field Branch 7 Name
       \\type object-list
       \\object-list Branches
   A9, \\field Branch 8 Name
       \\type object-list
       \\object-list Branches
   A10, \\field Branch 9 Name
        \\type object-list
        \\object-list Branches
   A11, \\field Branch 10 Name
        \\type object-list
        \\object-list Branches
   A12, \\field Branch 11 Name
        \\type object-list
        \\object-list Branches
   A13, \\field Branch 12 Name
       \\type object-list
        \\object-list Branches
   A14, \\field Branch 13 Name
        \\type object-list
        \\object-list Branches
   A15, \\field Branch 14 Name
        \\type object-list
        \\object-list Branches
   A16, \\field Branch 15 Name
        \\type object-list
        \\object-list Branches
   A17, \\field Branch 16 Name
        \\type object-list
        \\object-list Branches
   A18, \\field Branch 17 Name
        \\type object-list
        \\object-list Branches
   A19, \\field Branch 18 Name
        \\type object-list
        \\object-list Branches
   A20, \\field Branch 19 Name
        \\type object-list
        \\object-list Branches
   A21, \\field Branch 20 Name
        \\type object-list
        \\object-list Branches
   A22, \\field Branch 21 Name
        \\type object-list
        \\object-list Branches
   A23, \\field Branch 22 Name
        \\type object-list
        \\object-list Branches
   A24, \\field Branch 23 Name
        \\type object-list
        \\object-list Branches
   A25, \\field Branch 24 Name
        \\type object-list
        \\object-list Branches
   A26, \\field Branch 25 Name
        \\type object-list
        \\object-list Branches
   A27, \\field Branch 26 Name
        \\type object-list
        \\object-list Branches
   A28, \\field Branch 27 Name
        \\type object-list
        \\object-list Branches
   A29, \\field Branch 28 Name
        \\type object-list
        \\object-list Branches
   A30, \\field Branch 29 Name
        \\type object-list
        \\object-list Branches
   A31, \\field Branch 30 Name
        \\type object-list
        \\object-list Branches
   A32, \\field Branch 31 Name
        \\type object-list
        \\object-list Branches
   A33, \\field Branch 32 Name
        \\type object-list
        \\object-list Branches
   A34, \\field Branch 33 Name
        \\type object-list
        \\object-list Branches
   A35, \\field Branch 34 Name
        \\type object-list
        \\object-list Branches
   A36, \\field Branch 35 Name
        \\type object-list
        \\object-list Branches
   A37, \\field Branch 36 Name
        \\type object-list
        \\object-list Branches
   A38, \\field Branch 37 Name
        \\type object-list
        \\object-list Branches
   A39, \\field Branch 38 Name
        \\type object-list
        \\object-list Branches
   A40, \\field Branch 39 Name
        \\type object-list
        \\object-list Branches
   A41, \\field Branch 40 Name
        \\type object-list
        \\object-list Branches
   A42, \\field Branch 41 Name
        \\type object-list
        \\object-list Branches
   A43, \\field Branch 42 Name
        \\type object-list
        \\object-list Branches
   A44, \\field Branch 43 Name
        \\type object-list
        \\object-list Branches
   A45, \\field Branch 44 Name
        \\type object-list
        \\object-list Branches
   A46, \\field Branch 45 Name
        \\type object-list
        \\object-list Branches
   A47, \\field Branch 46 Name
        \\type object-list
        \\object-list Branches
   A48, \\field Branch 47 Name
        \\type object-list
        \\object-list Branches
   A49, \\field Branch 48 Name
        \\type object-list
        \\object-list Branches
   A50, \\field Branch 49 Name
        \\type object-list
        \\object-list Branches
   A51, \\field Branch 50 Name
        \\type object-list
        \\object-list Branches
   A52, \\field Branch 51 Name
        \\type object-list
        \\object-list Branches
   A53, \\field Branch 52 Name
        \\type object-list
        \\object-list Branches
   A54, \\field Branch 53 Name
        \\type object-list
        \\object-list Branches
   A55, \\field Branch 54 Name
        \\type object-list
        \\object-list Branches
   A56, \\field Branch 55 Name
        \\type object-list
        \\object-list Branches
   A57, \\field Branch 56 Name
        \\type object-list
        \\object-list Branches
   A58, \\field Branch 57 Name
        \\type object-list
        \\object-list Branches
   A59, \\field Branch 58 Name
        \\type object-list
        \\object-list Branches
   A60, \\field Branch 59 Name
        \\type object-list
        \\object-list Branches
   A61, \\field Branch 60 Name
        \\type object-list
        \\object-list Branches
   A62, \\field Branch 61 Name
        \\type object-list
        \\object-list Branches
   A63, \\field Branch 62 Name
        \\type object-list
        \\object-list Branches
   A64, \\field Branch 63 Name
        \\type object-list
        \\object-list Branches
   A65, \\field Branch 64 Name
        \\type object-list
        \\object-list Branches
   A66, \\field Branch 65 Name
        \\type object-list
        \\object-list Branches
   A67, \\field Branch 66 Name
        \\type object-list
        \\object-list Branches
   A68, \\field Branch 67 Name
        \\type object-list
        \\object-list Branches
   A69, \\field Branch 68 Name
        \\type object-list
        \\object-list Branches
   A70, \\field Branch 69 Name
        \\type object-list
        \\object-list Branches
   A71, \\field Branch 70 Name
        \\type object-list
        \\object-list Branches
   A72, \\field Branch 71 Name
        \\type object-list
        \\object-list Branches
   A73, \\field Branch 72 Name
        \\type object-list
        \\object-list Branches
   A74, \\field Branch 73 Name
        \\type object-list
        \\object-list Branches
   A75, \\field Branch 74 Name
        \\type object-list
        \\object-list Branches
   A76, \\field Branch 75 Name
        \\type object-list
        \\object-list Branches
   A77, \\field Branch 76 Name
        \\type object-list
        \\object-list Branches
   A78, \\field Branch 77 Name
        \\type object-list
        \\object-list Branches
   A79, \\field Branch 78 Name
        \\type object-list
        \\object-list Branches
   A80, \\field Branch 79 Name
        \\type object-list
        \\object-list Branches
   A81, \\field Branch 80 Name
        \\type object-list
        \\object-list Branches
   A82, \\field Branch 81 Name
        \\type object-list
        \\object-list Branches
   A83, \\field Branch 82 Name
        \\type object-list
        \\object-list Branches
   A84, \\field Branch 83 Name
        \\type object-list
        \\object-list Branches
   A85, \\field Branch 84 Name
        \\type object-list
        \\object-list Branches
   A86, \\field Branch 85 Name
        \\type object-list
        \\object-list Branches
   A87, \\field Branch 86 Name
        \\type object-list
        \\object-list Branches
   A88, \\field Branch 87 Name
        \\type object-list
        \\object-list Branches
   A89, \\field Branch 88 Name
        \\type object-list
        \\object-list Branches
   A90, \\field Branch 89 Name
        \\type object-list
        \\object-list Branches
   A91, \\field Branch 90 Name
        \\type object-list
        \\object-list Branches
   A92, \\field Branch 91 Name
        \\type object-list
        \\object-list Branches
   A93, \\field Branch 92 Name
        \\type object-list
        \\object-list Branches
   A94, \\field Branch 93 Name
        \\type object-list
        \\object-list Branches
   A95, \\field Branch 94 Name
        \\type object-list
        \\object-list Branches
   A96, \\field Branch 95 Name
        \\type object-list
        \\object-list Branches
   A97, \\field Branch 96 Name
        \\type object-list
        \\object-list Branches
   A98, \\field Branch 97 Name
        \\type object-list
        \\object-list Branches
   A99, \\field Branch 98 Name
        \\type object-list
        \\object-list Branches
  A100, \\field Branch 99 Name
        \\type object-list
        \\object-list Branches
  A101, \\field Branch 100 Name
        \\type object-list
        \\object-list Branches
  A102,A103,A104,A105,A106,A107,A108,A109,A110,A111, \\note fields as indicated
  A112,A113,A114,A115,A116,A117,A118,A119,A120,A121, \\note fields as indicated
  A122,A123,A124,A125,A126,A127,A128,A129,A130,A131, \\note fields as indicated
  A132,A133,A134,A135,A136,A137,A138,A139,A140,A141, \\note fields as indicated
  A142,A143,A144,A145,A146,A147,A148,A149,A150,A151, \\note fields as indicated
  A152,A153,A154,A155,A156,A157,A158,A159,A160,A161, \\note fields as indicated
  A162,A163,A164,A165,A166,A167,A168,A169,A170,A171, \\note fields as indicated
  A172,A173,A174,A175,A176,A177,A178,A179,A180,A181, \\note fields as indicated
  A182,A183,A184,A185,A186,A187,A188,A189,A190,A191, \\note fields as indicated
  A192,A193,A194,A195,A196,A197,A198,A199,A200,A201, \\note fields as indicated
  A202,A203,A204,A205,A206,A207,A208,A209,A210,A211, \\note fields as indicated
  A212,A213,A214,A215,A216,A217,A218,A219,A220,A221, \\note fields as indicated
  A222,A223,A224,A225,A226,A227,A228,A229,A230,A231, \\note fields as indicated
  A232,A233,A234,A235,A236,A237,A238,A239,A240,A241, \\note fields as indicated
  A242,A243,A244,A245,A246,A247,A248,A249,A250,A251, \\note fields as indicated
  A252,A253,A254,A255,A256,A257,A258,A259,A260,A261, \\note fields as indicated
  A262,A263,A264,A265,A266,A267,A268,A269,A270,A271, \\note fields as indicated
  A272,A273,A274,A275,A276,A277,A278,A279,A280,A281, \\note fields as indicated
  A282,A283,A284,A285,A286,A287,A288,A289,A290,A291, \\note fields as indicated
  A292,A293,A294,A295,A296,A297,A298,A299,A300,A301, \\note fields as indicated
  A302,A303,A304,A305,A306,A307,A308,A309,A310,A311, \\note fields as indicated
  A312,A313,A314,A315,A316,A317,A318,A319,A320,A321, \\note fields as indicated
  A322,A323,A324,A325,A326,A327,A328,A329,A330,A331, \\note fields as indicated
  A332,A333,A334,A335,A336,A337,A338,A339,A340,A341, \\note fields as indicated
  A342,A343,A344,A345,A346,A347,A348,A349,A350,A351, \\note fields as indicated
  A352,A353,A354,A355,A356,A357,A358,A359,A360,A361, \\note fields as indicated
  A362,A363,A364,A365,A366,A367,A368,A369,A370,A371, \\note fields as indicated
  A372,A373,A374,A375,A376,A377,A378,A379,A380,A381, \\note fields as indicated
  A382,A383,A384,A385,A386,A387,A388,A389,A390,A391, \\note fields as indicated
  A392,A393,A394,A395,A396,A397,A398,A399,A400,A401, \\note fields as indicated
  A402,A403,A404,A405,A406,A407,A408,A409,A410,A411, \\note fields as indicated
  A412,A413,A414,A415,A416,A417,A418,A419,A420,A421, \\note fields as indicated
  A422,A423,A424,A425,A426,A427,A428,A429,A430,A431, \\note fields as indicated
  A432,A433,A434,A435,A436,A437,A438,A439,A440,A441, \\note fields as indicated
  A442,A443,A444,A445,A446,A447,A448,A449,A450,A451, \\note fields as indicated
  A452,A453,A454,A455,A456,A457,A458,A459,A460,A461, \\note fields as indicated
  A462,A463,A464,A465,A466,A467,A468,A469,A470,A471, \\note fields as indicated
  A472,A473,A474,A475,A476,A477,A478,A479,A480,A481, \\note fields as indicated
  A482,A483,A484,A485,A486,A487,A488,A489,A490,A491, \\note fields as indicated
  A492,A493,A494,A495,A496,A497,A498,A499,A500,A501; \\note fields as indicated
Connector:Splitter,
  \\min-fields 3
       \\extensible:1 Just duplicate last field and comments (changing numbering, please)
       \\memo Split one air/water stream into N outlet streams.  Branch names cannot be duplicated
       \\memo within a single Splitter list.
   A1, \\field Name
        \\required-field
   A2, \\field Inlet Branch Name
        \\required-field
        \\type object-list
        \\object-list Branches
   A3, \\field Outlet Branch 1 Name
        \\begin-extensible
        \\required-field
        \\type object-list
        \\object-list Branches
   A4, \\field Outlet Branch 2 Name
        \\type object-list
        \\object-list Branches
   A5, \\field Outlet Branch 3 Name
        \\type object-list
        \\object-list Branches
   A6, \\field Outlet Branch 4 Name
        \\type object-list
        \\object-list Branches
   A7, \\field Outlet Branch 5 Name
        \\type object-list
        \\object-list Branches
   A8, \\field Outlet Branch 6 Name
        \\type object-list
        \\object-list Branches
   A9, \\field Outlet Branch 7 Name
        \\type object-list
        \\object-list Branches
   A10, \\field Outlet Branch 8 Name
        \\type object-list
        \\object-list Branches
   A11, \\field Outlet Branch 9 Name
        \\type object-list
        \\object-list Branches
   A12, \\field Outlet Branch 10 Name
        \\type object-list
        \\object-list Branches
   A13, \\field Outlet Branch 11 Name
        \\type object-list
        \\object-list Branches
   A14, \\field Outlet Branch 12 Name
        \\type object-list
        \\object-list Branches
   A15, \\field Outlet Branch 13 Name
        \\type object-list
        \\object-list Branches
   A16, \\field Outlet Branch 14 Name
        \\type object-list
        \\object-list Branches
   A17, \\field Outlet Branch 15 Name
        \\type object-list
        \\object-list Branches
   A18, \\field Outlet Branch 16 Name
        \\type object-list
        \\object-list Branches
   A19, \\field Outlet Branch 17 Name
        \\type object-list
        \\object-list Branches
   A20, \\field Outlet Branch 18 Name
        \\type object-list
        \\object-list Branches
   A21, \\field Outlet Branch 19 Name
        \\type object-list
        \\object-list Branches
   A22, \\field Outlet Branch 20 Name
        \\type object-list
        \\object-list Branches
   A23, \\field Outlet Branch 21 Name
        \\type object-list
        \\object-list Branches
   A24, \\field Outlet Branch 22 Name
        \\type object-list
        \\object-list Branches
   A25, \\field Outlet Branch 23 Name
        \\type object-list
        \\object-list Branches
   A26, \\field Outlet Branch 24 Name
        \\type object-list
        \\object-list Branches
   A27, \\field Outlet Branch 25 Name
        \\type object-list
        \\object-list Branches
   A28, \\field Outlet Branch 26 Name
        \\type object-list
        \\object-list Branches
   A29, \\field Outlet Branch 27 Name
        \\type object-list
        \\object-list Branches
   A30, \\field Outlet Branch 28 Name
        \\type object-list
        \\object-list Branches
   A31, \\field Outlet Branch 29 Name
        \\type object-list
        \\object-list Branches
   A32, \\field Outlet Branch 30 Name
        \\type object-list
        \\object-list Branches
   A33, \\field Outlet Branch 31 Name
        \\type object-list
        \\object-list Branches
   A34, \\field Outlet Branch 32 Name
        \\type object-list
        \\object-list Branches
   A35, \\field Outlet Branch 33 Name
        \\type object-list
        \\object-list Branches
   A36, \\field Outlet Branch 34 Name
        \\type object-list
        \\object-list Branches
   A37, \\field Outlet Branch 35 Name
        \\type object-list
        \\object-list Branches
   A38, \\field Outlet Branch 36 Name
        \\type object-list
        \\object-list Branches
   A39, \\field Outlet Branch 37 Name
        \\type object-list
        \\object-list Branches
   A40, \\field Outlet Branch 38 Name
        \\type object-list
        \\object-list Branches
   A41, \\field Outlet Branch 39 Name
        \\type object-list
        \\object-list Branches
   A42, \\field Outlet Branch 40 Name
        \\type object-list
        \\object-list Branches
   A43, \\field Outlet Branch 41 Name
        \\type object-list
        \\object-list Branches
   A44, \\field Outlet Branch 42 Name
        \\type object-list
        \\object-list Branches
   A45, \\field Outlet Branch 43 Name
        \\type object-list
        \\object-list Branches
   A46, \\field Outlet Branch 44 Name
        \\type object-list
        \\object-list Branches
   A47, \\field Outlet Branch 45 Name
        \\type object-list
        \\object-list Branches
   A48, \\field Outlet Branch 46 Name
        \\type object-list
        \\object-list Branches
   A49, \\field Outlet Branch 47 Name
        \\type object-list
        \\object-list Branches
   A50, \\field Outlet Branch 48 Name
        \\type object-list
        \\object-list Branches
   A51, \\field Outlet Branch 49 Name
        \\type object-list
        \\object-list Branches
   A52, \\field Outlet Branch 50 Name
        \\type object-list
        \\object-list Branches
   A53, \\field Outlet Branch 51 Name
        \\type object-list
        \\object-list Branches
   A54, \\field Outlet Branch 52 Name
        \\type object-list
        \\object-list Branches
   A55, \\field Outlet Branch 53 Name
        \\type object-list
        \\object-list Branches
   A56, \\field Outlet Branch 54 Name
        \\type object-list
        \\object-list Branches
   A57, \\field Outlet Branch 55 Name
        \\type object-list
        \\object-list Branches
   A58, \\field Outlet Branch 56 Name
        \\type object-list
        \\object-list Branches
   A59, \\field Outlet Branch 57 Name
        \\type object-list
        \\object-list Branches
   A60, \\field Outlet Branch 58 Name
        \\type object-list
        \\object-list Branches
   A61, \\field Outlet Branch 59 Name
        \\type object-list
        \\object-list Branches
   A62, \\field Outlet Branch 60 Name
        \\type object-list
        \\object-list Branches
   A63, \\field Outlet Branch 61 Name
        \\type object-list
        \\object-list Branches
   A64, \\field Outlet Branch 62 Name
        \\type object-list
        \\object-list Branches
   A65, \\field Outlet Branch 63 Name
        \\type object-list
        \\object-list Branches
   A66, \\field Outlet Branch 64 Name
        \\type object-list
        \\object-list Branches
   A67, \\field Outlet Branch 65 Name
        \\type object-list
        \\object-list Branches
   A68, \\field Outlet Branch 66 Name
        \\type object-list
        \\object-list Branches
   A69, \\field Outlet Branch 67 Name
        \\type object-list
        \\object-list Branches
   A70, \\field Outlet Branch 68 Name
        \\type object-list
        \\object-list Branches
   A71, \\field Outlet Branch 69 Name
        \\type object-list
        \\object-list Branches
   A72, \\field Outlet Branch 70 Name
        \\type object-list
        \\object-list Branches
   A73, \\field Outlet Branch 71 Name
        \\type object-list
        \\object-list Branches
   A74, \\field Outlet Branch 72 Name
        \\type object-list
        \\object-list Branches
   A75, \\field Outlet Branch 73 Name
        \\type object-list
        \\object-list Branches
   A76, \\field Outlet Branch 74 Name
        \\type object-list
        \\object-list Branches
   A77, \\field Outlet Branch 75 Name
        \\type object-list
        \\object-list Branches
   A78, \\field Outlet Branch 76 Name
        \\type object-list
        \\object-list Branches
   A79, \\field Outlet Branch 77 Name
        \\type object-list
        \\object-list Branches
   A80, \\field Outlet Branch 78 Name
        \\type object-list
        \\object-list Branches
   A81, \\field Outlet Branch 79 Name
        \\type object-list
        \\object-list Branches
   A82, \\field Outlet Branch 80 Name
        \\type object-list
        \\object-list Branches
   A83, \\field Outlet Branch 81 Name
        \\type object-list
        \\object-list Branches
   A84, \\field Outlet Branch 82 Name
        \\type object-list
        \\object-list Branches
   A85, \\field Outlet Branch 83 Name
        \\type object-list
        \\object-list Branches
   A86, \\field Outlet Branch 84 Name
        \\type object-list
        \\object-list Branches
   A87, \\field Outlet Branch 85 Name
        \\type object-list
        \\object-list Branches
   A88, \\field Outlet Branch 86 Name
        \\type object-list
        \\object-list Branches
   A89, \\field Outlet Branch 87 Name
        \\type object-list
        \\object-list Branches
   A90, \\field Outlet Branch 88 Name
        \\type object-list
        \\object-list Branches
   A91, \\field Outlet Branch 89 Name
        \\type object-list
        \\object-list Branches
   A92, \\field Outlet Branch 90 Name
        \\type object-list
        \\object-list Branches
   A93, \\field Outlet Branch 91 Name
        \\type object-list
        \\object-list Branches
   A94, \\field Outlet Branch 92 Name
        \\type object-list
        \\object-list Branches
   A95, \\field Outlet Branch 93 Name
        \\type object-list
        \\object-list Branches
   A96, \\field Outlet Branch 94 Name
        \\type object-list
        \\object-list Branches
   A97, \\field Outlet Branch 95 Name
        \\type object-list
        \\object-list Branches
   A98, \\field Outlet Branch 96 Name
        \\type object-list
        \\object-list Branches
   A99, \\field Outlet Branch 97 Name
        \\type object-list
        \\object-list Branches
  A100, \\field Outlet Branch 98 Name
        \\type object-list
        \\object-list Branches
  A101, \\field Outlet Branch 99 Name
        \\type object-list
        \\object-list Branches
  A102, \\field Outlet Branch 100 Name
        \\type object-list
        \\object-list Branches
  A103,A104,A105,A106,A107,A108,A109,A110,A111,A112, \\note fields as indicated
  A113,A114,A115,A116,A117,A118,A119,A120,A121,A122, \\note fields as indicated
  A123,A124,A125,A126,A127,A128,A129,A130,A131,A132, \\note fields as indicated
  A133,A134,A135,A136,A137,A138,A139,A140,A141,A142, \\note fields as indicated
  A143,A144,A145,A146,A147,A148,A149,A150,A151,A152, \\note fields as indicated
  A153,A154,A155,A156,A157,A158,A159,A160,A161,A162, \\note fields as indicated
  A163,A164,A165,A166,A167,A168,A169,A170,A171,A172, \\note fields as indicated
  A173,A174,A175,A176,A177,A178,A179,A180,A181,A182, \\note fields as indicated
  A183,A184,A185,A186,A187,A188,A189,A190,A191,A192, \\note fields as indicated
  A193,A194,A195,A196,A197,A198,A199,A200,A201,A202, \\note fields as indicated
  A203,A204,A205,A206,A207,A208,A209,A210,A211,A212, \\note fields as indicated
  A213,A214,A215,A216,A217,A218,A219,A220,A221,A222, \\note fields as indicated
  A223,A224,A225,A226,A227,A228,A229,A230,A231,A232, \\note fields as indicated
  A233,A234,A235,A236,A237,A238,A239,A240,A241,A242, \\note fields as indicated
  A243,A244,A245,A246,A247,A248,A249,A250,A251,A252, \\note fields as indicated
  A253,A254,A255,A256,A257,A258,A259,A260,A261,A262, \\note fields as indicated
  A263,A264,A265,A266,A267,A268,A269,A270,A271,A272, \\note fields as indicated
  A273,A274,A275,A276,A277,A278,A279,A280,A281,A282, \\note fields as indicated
  A283,A284,A285,A286,A287,A288,A289,A290,A291,A292, \\note fields as indicated
  A293,A294,A295,A296,A297,A298,A299,A300,A301,A302, \\note fields as indicated
  A303,A304,A305,A306,A307,A308,A309,A310,A311,A312, \\note fields as indicated
  A313,A314,A315,A316,A317,A318,A319,A320,A321,A322, \\note fields as indicated
  A323,A324,A325,A326,A327,A328,A329,A330,A331,A332, \\note fields as indicated
  A333,A334,A335,A336,A337,A338,A339,A340,A341,A342, \\note fields as indicated
  A343,A344,A345,A346,A347,A348,A349,A350,A351,A352, \\note fields as indicated
  A353,A354,A355,A356,A357,A358,A359,A360,A361,A362, \\note fields as indicated
  A363,A364,A365,A366,A367,A368,A369,A370,A371,A372, \\note fields as indicated
  A373,A374,A375,A376,A377,A378,A379,A380,A381,A382, \\note fields as indicated
  A383,A384,A385,A386,A387,A388,A389,A390,A391,A392, \\note fields as indicated
  A393,A394,A395,A396,A397,A398,A399,A400,A401,A402, \\note fields as indicated
  A403,A404,A405,A406,A407,A408,A409,A410,A411,A412, \\note fields as indicated
  A413,A414,A415,A416,A417,A418,A419,A420,A421,A422, \\note fields as indicated
  A423,A424,A425,A426,A427,A428,A429,A430,A431,A432, \\note fields as indicated
  A433,A434,A435,A436,A437,A438,A439,A440,A441,A442, \\note fields as indicated
  A443,A444,A445,A446,A447,A448,A449,A450,A451,A452, \\note fields as indicated
  A453,A454,A455,A456,A457,A458,A459,A460,A461,A462, \\note fields as indicated
  A463,A464,A465,A466,A467,A468,A469,A470,A471,A472, \\note fields as indicated
  A473,A474,A475,A476,A477,A478,A479,A480,A481,A482, \\note fields as indicated
  A483,A484,A485,A486,A487,A488,A489,A490,A491,A492, \\note fields as indicated
  A493,A494,A495,A496,A497,A498,A499,A500,A501,A502; \\note fields as indicated

Connector:Mixer,
  \\min-fields 3
       \\extensible:1 Just duplicate last field and comments (changing numbering, please)
       \\memo Mix N inlet air/water streams into one.  Branch names cannot be duplicated within
       \\memo a single mixer list.
   A1 , \\field Name
        \\required-field
   A2 , \\field Outlet Branch Name
        \\required-field
        \\type object-list
        \\object-list Branches
   A3 , \\field Inlet Branch 1 Name
        \\begin-extensible
        \\required-field
        \\type object-list
        \\object-list Branches
   A4 , \\field Inlet Branch 2 Name
        \\type object-list
        \\object-list Branches
   A5 , \\field Inlet Branch 3 Name
        \\type object-list
        \\object-list Branches
   A6 , \\field Inlet Branch 4 Name
        \\type object-list
        \\object-list Branches
   A7 , \\field Inlet Branch 5 Name
        \\type object-list
        \\object-list Branches
   A8 , \\field Inlet Branch 6 Name
        \\type object-list
        \\object-list Branches
   A9 , \\field Inlet Branch 7 Name
        \\type object-list
        \\object-list Branches
   A10, \\field Inlet Branch 8 Name
        \\type object-list
        \\object-list Branches
   A11, \\field Inlet Branch 9 Name
        \\type object-list
        \\object-list Branches
   A12, \\field Inlet Branch 10 Name
        \\type object-list
        \\object-list Branches
   A13, \\field Inlet Branch 11 Name
        \\type object-list
        \\object-list Branches
   A14, \\field Inlet Branch 12 Name
        \\type object-list
        \\object-list Branches
   A15, \\field Inlet Branch 13 Name
        \\type object-list
        \\object-list Branches
   A16, \\field Inlet Branch 14 Name
        \\type object-list
        \\object-list Branches
   A17, \\field Inlet Branch 15 Name
        \\type object-list
        \\object-list Branches
   A18, \\field Inlet Branch 16 Name
        \\type object-list
        \\object-list Branches
   A19, \\field Inlet Branch 17 Name
        \\type object-list
        \\object-list Branches
   A20, \\field Inlet Branch 18 Name
        \\type object-list
        \\object-list Branches
   A21, \\field Inlet Branch 19 Name
        \\type object-list
        \\object-list Branches
   A22, \\field Inlet Branch 20 Name
        \\type object-list
        \\object-list Branches
   A23, \\field Inlet Branch 21 Name
        \\type object-list
        \\object-list Branches
   A24, \\field Inlet Branch 22 Name
        \\type object-list
        \\object-list Branches
   A25, \\field Inlet Branch 23 Name
        \\type object-list
        \\object-list Branches
   A26, \\field Inlet Branch 24 Name
        \\type object-list
        \\object-list Branches
   A27, \\field Inlet Branch 25 Name
        \\type object-list
        \\object-list Branches
   A28, \\field Inlet Branch 26 Name
        \\type object-list
        \\object-list Branches
   A29, \\field Inlet Branch 27 Name
        \\type object-list
        \\object-list Branches
   A30, \\field Inlet Branch 28 Name
        \\type object-list
        \\object-list Branches
   A31, \\field Inlet Branch 29 Name
        \\type object-list
        \\object-list Branches
   A32, \\field Inlet Branch 30 Name
        \\type object-list
        \\object-list Branches
   A33, \\field Inlet Branch 31 Name
        \\type object-list
        \\object-list Branches
   A34, \\field Inlet Branch 32 Name
        \\type object-list
        \\object-list Branches
   A35, \\field Inlet Branch 33 Name
        \\type object-list
        \\object-list Branches
   A36, \\field Inlet Branch 34 Name
        \\type object-list
        \\object-list Branches
   A37, \\field Inlet Branch 35 Name
        \\type object-list
        \\object-list Branches
   A38, \\field Inlet Branch 36 Name
        \\type object-list
        \\object-list Branches
   A39, \\field Inlet Branch 37 Name
        \\type object-list
        \\object-list Branches
   A40, \\field Inlet Branch 38 Name
        \\type object-list
        \\object-list Branches
   A41, \\field Inlet Branch 39 Name
        \\type object-list
        \\object-list Branches
   A42, \\field Inlet Branch 40 Name
        \\type object-list
        \\object-list Branches
   A43, \\field Inlet Branch 41 Name
        \\type object-list
        \\object-list Branches
   A44, \\field Inlet Branch 42 Name
        \\type object-list
        \\object-list Branches
   A45, \\field Inlet Branch 43 Name
        \\type object-list
        \\object-list Branches
   A46, \\field Inlet Branch 44 Name
        \\type object-list
        \\object-list Branches
   A47, \\field Inlet Branch 45 Name
        \\type object-list
        \\object-list Branches
   A48, \\field Inlet Branch 46 Name
        \\type object-list
        \\object-list Branches
   A49, \\field Inlet Branch 47 Name
        \\type object-list
        \\object-list Branches
   A50, \\field Inlet Branch 48 Name
        \\type object-list
        \\object-list Branches
   A51, \\field Inlet Branch 49 Name
        \\type object-list
        \\object-list Branches
   A52, \\field Inlet Branch 50 Name
        \\type object-list
        \\object-list Branches
   A53, \\field Inlet Branch 51 Name
        \\type object-list
        \\object-list Branches
   A54, \\field Inlet Branch 52 Name
        \\type object-list
        \\object-list Branches
   A55, \\field Inlet Branch 53 Name
        \\type object-list
        \\object-list Branches
   A56, \\field Inlet Branch 54 Name
        \\type object-list
        \\object-list Branches
   A57, \\field Inlet Branch 55 Name
        \\type object-list
        \\object-list Branches
   A58, \\field Inlet Branch 56 Name
        \\type object-list
        \\object-list Branches
   A59, \\field Inlet Branch 57 Name
        \\type object-list
        \\object-list Branches
   A60, \\field Inlet Branch 58 Name
        \\type object-list
        \\object-list Branches
   A61, \\field Inlet Branch 59 Name
        \\type object-list
        \\object-list Branches
   A62, \\field Inlet Branch 60 Name
        \\type object-list
        \\object-list Branches
   A63, \\field Inlet Branch 61 Name
        \\type object-list
        \\object-list Branches
   A64, \\field Inlet Branch 62 Name
        \\type object-list
        \\object-list Branches
   A65, \\field Inlet Branch 63 Name
        \\type object-list
        \\object-list Branches
   A66, \\field Inlet Branch 64 Name
        \\type object-list
        \\object-list Branches
   A67, \\field Inlet Branch 65 Name
        \\type object-list
        \\object-list Branches
   A68, \\field Inlet Branch 66 Name
        \\type object-list
        \\object-list Branches
   A69, \\field Inlet Branch 67 Name
        \\type object-list
        \\object-list Branches
   A70, \\field Inlet Branch 68 Name
        \\type object-list
        \\object-list Branches
   A71, \\field Inlet Branch 69 Name
        \\type object-list
        \\object-list Branches
   A72, \\field Inlet Branch 70 Name
        \\type object-list
        \\object-list Branches
   A73, \\field Inlet Branch 71 Name
        \\type object-list
        \\object-list Branches
   A74, \\field Inlet Branch 72 Name
        \\type object-list
        \\object-list Branches
   A75, \\field Inlet Branch 73 Name
        \\type object-list
        \\object-list Branches
   A76, \\field Inlet Branch 74 Name
        \\type object-list
        \\object-list Branches
   A77, \\field Inlet Branch 75 Name
        \\type object-list
        \\object-list Branches
   A78, \\field Inlet Branch 76 Name
        \\type object-list
        \\object-list Branches
   A79, \\field Inlet Branch 77 Name
        \\type object-list
        \\object-list Branches
   A80, \\field Inlet Branch 78 Name
        \\type object-list
        \\object-list Branches
   A81, \\field Inlet Branch 79 Name
        \\type object-list
        \\object-list Branches
   A82, \\field Inlet Branch 80 Name
        \\type object-list
        \\object-list Branches
   A83, \\field Inlet Branch 81 Name
        \\type object-list
        \\object-list Branches
   A84, \\field Inlet Branch 82 Name
        \\type object-list
        \\object-list Branches
   A85, \\field Inlet Branch 83 Name
        \\type object-list
        \\object-list Branches
   A86, \\field Inlet Branch 84 Name
        \\type object-list
        \\object-list Branches
   A87, \\field Inlet Branch 85 Name
        \\type object-list
        \\object-list Branches
   A88, \\field Inlet Branch 86 Name
        \\type object-list
        \\object-list Branches
   A89, \\field Inlet Branch 87 Name
        \\type object-list
        \\object-list Branches
   A90, \\field Inlet Branch 88 Name
        \\type object-list
        \\object-list Branches
   A91, \\field Inlet Branch 89 Name
        \\type object-list
        \\object-list Branches
   A92, \\field Inlet Branch 90 Name
        \\type object-list
        \\object-list Branches
   A93, \\field Inlet Branch 91 Name
        \\type object-list
        \\object-list Branches
   A94, \\field Inlet Branch 92 Name
        \\type object-list
        \\object-list Branches
   A95, \\field Inlet Branch 93 Name
        \\type object-list
        \\object-list Branches
   A96, \\field Inlet Branch 94 Name
        \\type object-list
        \\object-list Branches
   A97, \\field Inlet Branch 95 Name
        \\type object-list
        \\object-list Branches
   A98, \\field Inlet Branch 96 Name
        \\type object-list
        \\object-list Branches
   A99, \\field Inlet Branch 97 Name
        \\type object-list
        \\object-list Branches
  A100, \\field Inlet Branch 98 Name
        \\type object-list
        \\object-list Branches
  A101, \\field Inlet Branch 99 Name
        \\type object-list
        \\object-list Branches
  A102, \\field Inlet Branch 100 Name
        \\type object-list
        \\object-list Branches
  A103,A104,A105,A106,A107,A108,A109,A110,A111,A112, \\note fields as indicated
  A113,A114,A115,A116,A117,A118,A119,A120,A121,A122, \\note fields as indicated
  A123,A124,A125,A126,A127,A128,A129,A130,A131,A132, \\note fields as indicated
  A133,A134,A135,A136,A137,A138,A139,A140,A141,A142, \\note fields as indicated
  A143,A144,A145,A146,A147,A148,A149,A150,A151,A152, \\note fields as indicated
  A153,A154,A155,A156,A157,A158,A159,A160,A161,A162, \\note fields as indicated
  A163,A164,A165,A166,A167,A168,A169,A170,A171,A172, \\note fields as indicated
  A173,A174,A175,A176,A177,A178,A179,A180,A181,A182, \\note fields as indicated
  A183,A184,A185,A186,A187,A188,A189,A190,A191,A192, \\note fields as indicated
  A193,A194,A195,A196,A197,A198,A199,A200,A201,A202, \\note fields as indicated
  A203,A204,A205,A206,A207,A208,A209,A210,A211,A212, \\note fields as indicated
  A213,A214,A215,A216,A217,A218,A219,A220,A221,A222, \\note fields as indicated
  A223,A224,A225,A226,A227,A228,A229,A230,A231,A232, \\note fields as indicated
  A233,A234,A235,A236,A237,A238,A239,A240,A241,A242, \\note fields as indicated
  A243,A244,A245,A246,A247,A248,A249,A250,A251,A252, \\note fields as indicated
  A253,A254,A255,A256,A257,A258,A259,A260,A261,A262, \\note fields as indicated
  A263,A264,A265,A266,A267,A268,A269,A270,A271,A272, \\note fields as indicated
  A273,A274,A275,A276,A277,A278,A279,A280,A281,A282, \\note fields as indicated
  A283,A284,A285,A286,A287,A288,A289,A290,A291,A292, \\note fields as indicated
  A293,A294,A295,A296,A297,A298,A299,A300,A301,A302, \\note fields as indicated
  A303,A304,A305,A306,A307,A308,A309,A310,A311,A312, \\note fields as indicated
  A313,A314,A315,A316,A317,A318,A319,A320,A321,A322, \\note fields as indicated
  A323,A324,A325,A326,A327,A328,A329,A330,A331,A332, \\note fields as indicated
  A333,A334,A335,A336,A337,A338,A339,A340,A341,A342, \\note fields as indicated
  A343,A344,A345,A346,A347,A348,A349,A350,A351,A352, \\note fields as indicated
  A353,A354,A355,A356,A357,A358,A359,A360,A361,A362, \\note fields as indicated
  A363,A364,A365,A366,A367,A368,A369,A370,A371,A372, \\note fields as indicated
  A373,A374,A375,A376,A377,A378,A379,A380,A381,A382, \\note fields as indicated
  A383,A384,A385,A386,A387,A388,A389,A390,A391,A392, \\note fields as indicated
  A393,A394,A395,A396,A397,A398,A399,A400,A401,A402, \\note fields as indicated
  A403,A404,A405,A406,A407,A408,A409,A410,A411,A412, \\note fields as indicated
  A413,A414,A415,A416,A417,A418,A419,A420,A421,A422, \\note fields as indicated
  A423,A424,A425,A426,A427,A428,A429,A430,A431,A432, \\note fields as indicated
  A433,A434,A435,A436,A437,A438,A439,A440,A441,A442, \\note fields as indicated
  A443,A444,A445,A446,A447,A448,A449,A450,A451,A452, \\note fields as indicated
  A453,A454,A455,A456,A457,A458,A459,A460,A461,A462, \\note fields as indicated
  A463,A464,A465,A466,A467,A468,A469,A470,A471,A472, \\note fields as indicated
  A473,A474,A475,A476,A477,A478,A479,A480,A481,A482, \\note fields as indicated
  A483,A484,A485,A486,A487,A488,A489,A490,A491,A492, \\note fields as indicated
  A493,A494,A495,A496,A497,A498,A499,A500,A501,A502; \\note fields as indicated

ConnectorList,
        \\memo only two connectors allowed per loop
        \\memo if two entered, one must be Connector:Splitter and one must be Connector:Mixer
    A1, \\field Name
        \\required-field
        \\reference ConnectorLists
    A2, \\field Connector 1 Object Type
        \\required-field
        \\type choice
        \\key Connector:Splitter
        \\key Connector:Mixer
    A3, \\field Connector 1 Name
        \\required-field
    A4, \\field Connector 2 Object Type
        \\type choice
        \\key Connector:Splitter
        \\key Connector:Mixer
    A5; \\field Connector 2 Name

PlantLoop,
  A1 , \\field Name
        \\required-field
       \\reference PlantLoops
  A2 , \\field Fluid Type
        \\required-field
        \\type choice
        \\key Water
        \\key Steam
        \\default Water
  A3 , \\field Plant Equipment Operation Scheme Name
        \\required-field
        \\type object-list
        \\object-list PlantOperationSchemes
  A4 , \\field Loop Temperature Setpoint Node Name
        \\required-field
  N1 , \\field Maximum Loop Temperature
        \\required-field
        \\units C
  N2 , \\field Minimum Loop Temperature
        \\required-field
        \\units C
  N3 , \\field Maximum Loop Flow Rate
        \\required-field
        \\type real
        \\units m3/s
        \\autosizable
        \\minimum 0
        \\ip-units gal/min
  N4 , \\field Minimum Loop Flow Rate
        \\type real
        \\units m3/s
        \\default 0.0
        \\ip-units gal/min
  N5 , \\field Plant Loop Volume
        \\type real
        \\units m3
        \\autocalculatable
        \\minimum 0.0
        \\default Autocalculate
        \\ip-units gal
  A5,  \\field Plant Side Inlet Node Name
        \\required-field
  A6,  \\field Plant Side Outlet Node Name
        \\required-field
  A7,  \\field Plant Side Branch List Name
        \\required-field
        \\type object-list
        \\object-list BranchLists
  A8,  \\field Plant Side Connector List Name
        \\type object-list
        \\object-list ConnectorLists
  A9,  \\field Demand Side Inlet Node Name
        \\required-field
  A10, \\field Demand Side Outlet Node Name
        \\required-field
  A11, \\field Demand Side Branch List Name
        \\required-field
        \\type object-list
        \\object-list BranchLists
  A12, \\field Demand Side Connector List Name
        \\type object-list
        \\object-list ConnectorLists
  A13, \\field Load Distribution Scheme
        \\type choice
        \\key Optimal
        \\key Sequential
        \\key Uniform
        \\default Sequential
  A14, \\field Availability Manager List Name
        \\type object-list
        \\object-list SystemAvailabilityManagerLists
  A15, \\field Plant Loop Demand Calculation Scheme
        \\type choice
        \\key SingleSetpoint
        \\key DualSetpointDeadband
        \\default SingleSetpoint
  A16,  \\field Common Pipe Simulation
        \\note Specifies a primary-secondary loop configuration. The plant side is the
        \\note primary loop, and the demand side is the secondary loop.
        \\note A secondary supply pump is required on the demand side.
        \\note None = Primary-only, no secondary simulation
        \\note CommonPipe = Primary-secondary with no temperature control at primary-secondary interface
        \\note TwoWayCommonPipe = Primary-secondary with control of secondary supply temperature or
        \\note primary return temperature (requires a setpoint be placed on the
        \\note plant side or demand side inlet node).
        \\type choice
        \\key CommonPipe
        \\key TwoWayCommonPipe
        \\key None
        \\default None
  A17;  \\field Pressure Simulation Type
        \\type choice
        \\key PumpPowerCorrection
        \\key LoopFlowCorrection
        \\key None
        \\default None

"""

def test_flattencopy():
    """py.test for flattencopy"""
    tdata = (([1,2], [1,2]), #lst , nlst
    ([1,2,[3,4]], [1,2,3,4]), #lst , nlst
    ([1,2,[3,[4,5,6],7,8]], [1,2,3,4,5,6,7,8]), #lst , nlst
    ([1,2,[3,[4,5,[6,7],8],9]], [1,2,3,4,5,6,7,8,9]), #lst , nlst
    )
    for lst , nlst in tdata:
        result = hvacbuilder.flattencopy(lst)
        assert result == nlst

"""BRANCH,sb0,0,,Pipe:Adiabatic,sb0_pipe,p_loop Supply Inlet,sb0_pipe_outlet,Bypass;BRANCH,sb1,0,,Pipe:Adiabatic,sb1_pipe,sb1_pipe_inlet,sb1_pipe_outlet,Bypass;BRANCH,sb2,0,,Pipe:Adiabatic,sb2_pipe,sb2_pipe_inlet,sb2_pipe_outlet,Bypass;BRANCH,sb3,0,,Pipe:Adiabatic,sb3_pipe,sb3_pipe_inlet,sb3_pipe_outlet,Bypass;BRANCH,sb4,0,,Pipe:Adiabatic,sb4_pipe,sb4_pipe_inlet,p_loop Supply Outlet,Bypass;BRANCH,db0,0,,Pipe:Adiabatic,db0_pipe,p_loop Demand Inlet,db0_pipe_outlet,Bypass;BRANCH,db1,0,,Pipe:Adiabatic,db1_pipe,db1_pipe_inlet,db1_pipe_outlet,Bypass;BRANCH,db2,0,,Pipe:Adiabatic,db2_pipe,db2_pipe_inlet,db2_pipe_outlet,Bypass;BRANCH,db3,0,,Pipe:Adiabatic,db3_pipe,db3_pipe_inlet,db3_pipe_outlet,Bypass;BRANCH,db4,0,,Pipe:Adiabatic,db4_pipe,db4_pipe_inlet,p_loop Demand Outlet,Bypass;BRANCHLIST,p_loop Supply Branchs,sb1,sb2,sb3;BRANCHLIST,p_loop Demand Branchs,db1,db2,db3;CONNECTOR:SPLITTER,p_loop_supply_splitter,sb0,sb1,sb2,sb3;CONNECTOR:SPLITTER,p_loop_demand_splitter,db0,db1,db2,db3;CONNECTOR:MIXER,p_loop_supply_mixer,sb4,sb1,sb2,sb3;CONNECTOR:MIXER,p_loop_demand_mixer,db4,db1,db2,db3;CONNECTORLIST,p_loop Supply Connectors,Connector:Splitter,p_loop_supply_splitter,Connector:Mixer,p_loop_supply_mixer;CONNECTORLIST,p_loop Demand Connectors,Connector:Splitter,p_loop_demand_splitter,Connector:Mixer,p_loop_demand_mixer;PLANTLOOP,p_loop,Water,,,,,,0.0,Autocalculate,p_loop Supply Inlet,p_loop Supply Outlet,p_loop Supply Branchs,p_loop Supply Connectors,p_loop Demand Inlet,p_loop Demand Outlet,p_loop Demand Branchs,p_loop Demand Connectors,Sequential,,SingleSetpoint,None,None;"""

def test_makeplantloop():
    """pytest for makeplantloop"""
    tdata = (("", 
    "p_loop",
    ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'],
    ['db0', ['db1', 'db2', 'db3'], 'db4'],
    """BRANCH,sb0,0,,Pipe:Adiabatic,sb0_pipe,p_loop Supply Inlet,sb0_pipe_outlet,Bypass;BRANCH,sb1,0,,Pipe:Adiabatic,sb1_pipe,sb1_pipe_inlet,sb1_pipe_outlet,Bypass;BRANCH,sb2,0,,Pipe:Adiabatic,sb2_pipe,sb2_pipe_inlet,sb2_pipe_outlet,Bypass;BRANCH,sb3,0,,Pipe:Adiabatic,sb3_pipe,sb3_pipe_inlet,sb3_pipe_outlet,Bypass;BRANCH,sb4,0,,Pipe:Adiabatic,sb4_pipe,sb4_pipe_inlet,p_loop Supply Outlet,Bypass;BRANCH,db0,0,,Pipe:Adiabatic,db0_pipe,p_loop Demand Inlet,db0_pipe_outlet,Bypass;BRANCH,db1,0,,Pipe:Adiabatic,db1_pipe,db1_pipe_inlet,db1_pipe_outlet,Bypass;BRANCH,db2,0,,Pipe:Adiabatic,db2_pipe,db2_pipe_inlet,db2_pipe_outlet,Bypass;BRANCH,db3,0,,Pipe:Adiabatic,db3_pipe,db3_pipe_inlet,db3_pipe_outlet,Bypass;BRANCH,db4,0,,Pipe:Adiabatic,db4_pipe,db4_pipe_inlet,p_loop Demand Outlet,Bypass;BRANCHLIST,p_loop Supply Branchs,sb1,sb2,sb3;BRANCHLIST,p_loop Demand Branchs,db1,db2,db3;CONNECTOR:SPLITTER,p_loop_supply_splitter,sb0,sb1,sb2,sb3;CONNECTOR:SPLITTER,p_loop_demand_splitter,db0,db1,db2,db3;CONNECTOR:MIXER,p_loop_supply_mixer,sb4,sb1,sb2,sb3;CONNECTOR:MIXER,p_loop_demand_mixer,db4,db1,db2,db3;CONNECTORLIST,p_loop Supply Connectors,Connector:Splitter,p_loop_supply_splitter,Connector:Mixer,p_loop_supply_mixer;CONNECTORLIST,p_loop Demand Connectors,Connector:Splitter,p_loop_demand_splitter,Connector:Mixer,p_loop_demand_mixer;PLANTLOOP,p_loop,Water,,,,,,0.0,Autocalculate,p_loop Supply Inlet,p_loop Supply Outlet,p_loop Supply Branchs,p_loop Supply Connectors,p_loop Demand Inlet,p_loop Demand Outlet,p_loop Demand Branchs,p_loop Demand Connectors,Sequential,,SingleSetpoint,None,None;"""
    ), # blankidf, loopname, sloop, dloop, nidf
    )
    for blankidf, loopname, sloop, dloop, nidf in tdata:
        # iddfile = "./walls%s.idd" % (random.randint(11111, 99999))
        # fname = "%sout.idf" % (random.randint(11111, 99999))
        # iddfile = "%senrergy.idd" % (random.randint(11111, 99999))
        # ntxtfname = "%snout.idf" % (random.randint(11111, 99999))
        # open(fname, 'w').write(blankidf)
        # open(iddfile, 'w').write(iddtxt)
        # IDF.setiddname(iddfile)
        
        iddhandle = StringIO(iddtxt)
        IDF.setiddname(iddhandle)
        fnamehandle = StringIO("")
        idf1 = IDF(fnamehandle)
        # - 
        loopname = "p_loop"
        sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
        dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
        hvacbuilder.makeplantloop(idf1, loopname, sloop, dloop)
        # - 
        result = idf1.idfstr()
        # now nidf read as idf, get it's tr repr and compare
        nidfhandle = StringIO(nidf)
        idf2 = IDF(nidfhandle)
        idf2str = idf2.idfstr()
        # print result
        # print '*' * 25
        # print idf2str
        assert result == idf2str
        
        # idf1txt = open(fname, 'r').read()
        # open(ntxtfname, 'w').write(str(idf1))
        # nidf = IDF(ntxtfname)
        # nidf.save()
        # nidftxt = open(ntxtfname, 'r').read()
        # assert idf1txt ==  nidftxt
        # os.remove(fname)
        # os.remove(iddfile)
        # os.remove(ntxtfname)

        