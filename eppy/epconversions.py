# Copyright (c) 2023-2024 Santosh Philip
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""Conversion functions for EnergyPlus"""

from typing import Dict
from typing import Optional
from typing import Union
from typing import Any

UnitDictValVal = Optional[Union[str, float, None, list[str]]]
UnitDictVal = Dict[str, UnitDictValVal]
UnitDict = Dict[str, UnitDictVal]

TXT = """! Default IP conversions (no ip-units necessary)
!      $/(m3/s)               =>   $/(ft3/min)         0.000472000059660808
!      $/(W/K)                =>   $/(Btu/h-F)         0.52667614683731
!      $/kW                   =>   $/(kBtuh/h)         0.293083235638921
!      $/m2                   =>   $/ft2               0.0928939733269818
!      $/m3                   =>   $/ft3               0.0283127014102352
!      (kg/s)/W               =>   (lbm/sec)/(Btu/hr)  0.646078115385742
!      1/K                    =>   1/F                 0.555555555555556
!      1/m                    =>   1/ft                0.3048
!      A/K                    =>   A/F                 0.555555555555556
!      C                      =>   F                   1.8 (plus 32)
!      cm                     =>   in                  0.3937
!      cm2                    =>   inch2               0.15500031000062
!      deltaC                 =>   deltaF              1.8
!      deltaC/hr              =>   deltaF/hr           1.8
!      deltaJ/kg              =>   deltaBtu/lb         0.0004299
!      g/GJ                   =>   lb/MWh              0.00793664091373665
!      g/kg                   =>   grains/lb           7
!      g/MJ                   =>   lb/MWh              7.93664091373665
!      g/mol                  =>   lb/mol              0.0022046
!      g/m-s                  =>   lb/ft-s             0.000671968949659
!      g/m-s-K                =>   lb/ft-s-F           0.000373574867724868
!      GJ                     =>   ton-hrs             78.9889415481832
!      J                      =>   Wh                  0.000277777777777778
!      J/K                    =>   Btu/F               526.565
!      J/kg                   =>   Btu/lb              0.00042986
!      J/kg-K                 =>   Btu/lb-F            0.000239005736137667
!      J/kg-K2                =>   Btu/lb-F2           0.000132889924714692
!      J/kg-K3                =>   Btu/lb-F3           7.38277359526066E-05
!      J/m2-K                 =>   Btu/ft2-F           4.89224766847393E-05
!      J/m3                   =>   Btu/ft3             2.68096514745308E-05
!      J/m3-K                 =>   Btu/ft3-F           1.49237004739337E-05
!      K                      =>   R                   1.8
!      K/m                    =>   F/ft                0.54861322767449
!      kg                     =>   lb                  2.2046
!      kg/J                   =>   lb/Btu              2325.83774250441
!      kg/kg-K                =>   lb/lb-F             0.555555555555556
!      kg/m                   =>   lb/ft               0.67196893069637
!      kg/m2                  =>   lb/ft2              0.204794053596664
!      kg/m3                  =>   lb/ft3              0.062428
!      kg/m-s                 =>   lb/ft-s             0.67196893069637
!      kg/m-s-K               =>   lb/ft-s-F           0.373316072609094
!      kg/m-s-K2              =>   lb/ft-s-F2          0.207397818116164
!      kg/Pa-s-m2             =>   lb/psi-s-ft2        1412.00523459398
!      kg/s                   =>   lb/s                2.20462247603796
!      kg/s2                  =>   lb/s2               2.2046
!      kg/s-m                 =>   lb/s-ft             0.67196893069637
!      kJ/kg                  =>   Btu/lb              0.429925
!      kPa                    =>   psi                 0.145038
!      L/day                  =>   pint/day            2.11337629827348
!      L/GJ                   =>   gal/kWh             0.000951022349025202
!      L/kWh                  =>   pint/kWh            2.11337629827348
!      L/MJ                   =>   gal/kWh             0.951022349025202
!      lux                    =>   foot-candles        0.092902267
!      m                      =>   ft                  3.28083989501312
!      m/hr                   =>   ft/hr               3.28083989501312
!      m/s                    =>   ft/min              196.850393700787
!      m/s                    =>   miles/hr            2.2369362920544
!      m/yr                   =>   inch/yr             39.3700787401575
!      m2                     =>   ft2                 10.7639104167097
!      m2/m                   =>   ft2/ft              3.28083989501312
!      m2/person              =>   ft2/person          10.764961
!      m2/s                   =>   ft2/s               10.7639104167097
!      m2-K/W                 =>   ft2-F-hr/Btu        5.678263
!      m3                     =>   ft3                 35.3146667214886
!      m3                     =>   gal                 264.172037284185
!      m3/GJ                  =>   ft3/MWh             127.13292
!      m3/hr                  =>   ft3/hr              35.3146667214886
!      m3/hr-m2               =>   ft3/hr-ft2          3.28083989501312
!      m3/hr-person           =>   ft3/hr-person       35.3146667214886
!      m3/kg                  =>   ft3/lb              16.018
!      m3/m2                  =>   ft3/ft2             3.28083989501312
!      m3/MJ                  =>   ft3/kWh             127.13292
!      m3/person              =>   ft3/person          35.3146667214886
!      m3/s                   =>   ft3/min             2118.88000328931
!      m3/s-m                 =>   ft3/min-ft          645.89
!      m3/s-m2                =>   ft3/min-ft2         196.85
!      m3/s-person            =>   ft3/min-person      2118.6438
!      m3/s-W                 =>   (ft3/min)/(Btu/h)   621.099127332943
!      N-m                    =>   lbf-in              8.85074900525547
!      N-s/m2                 =>   lbf-s/ft2           0.0208857913669065
!      Pa                     =>   psi                 0.000145037743897283
!      percent/K              =>   percent/F           0.555555555555556
!      person/m2              =>   person/ft2          0.0928939733269818
!      s/m                    =>   s/ft                0.3048
!      V/K                    =>   V/F                 0.555555555555556
!      W                      =>   Btu/h               3.4121412858518
!      W/((m3/s)-Pa)          =>   W/((gal/min)-ftH20) 0.188582274697355
!      W/((m3/s)-Pa)          =>   W/((ft3/min)-inH2O) 0.117556910599482
!      W/(m3/s)               =>   W/(ft3/min)         0.0004719475
!      W/K                    =>   Btu/h-F             1.89563404769544
!      W/m                    =>   Btu/h-ft            1.04072
!      W/m2                   =>   Btu/h-ft2           0.316957210776545
!      W/m2                   =>   W/ft2               0.09290304
!      W/m2-K                 =>   Btu/h-ft2-F         0.176110194261872
!      W/m2-K2                =>   Btu/h-ft2-F2        0.097826
!      W/m-K                  =>   Btu-in/h-ft2-F      6.93481276005548
!      W/m-K2                 =>   Btu/h-F2-ft         0.321418310071648
!      W/m-K3                 =>   Btu/h-F3-ft         0.178565727817582
!      W/person               =>   Btu/h-person        3.4121412858518
!
! Other conversions supported (needs the \\ip-units code)
!
!      kPa                    =>   inHg                0.29523
!      m                      =>   in                  39.3700787401575
!      m3/hr                  =>   gal/hr              264.172037284185
!      m3/hr-m2               =>   gal/hr-ft2          24.5423853466941
!      m3/hr-person           =>   gal/hr-person       264.172037284185
!      m3/m2                  =>   gal/ft2             24.5423853466941
!      m3/person              =>   gal/person          264.172037284185
!      m3/s                   =>   gal/min             15850.3222370511
!      m3/s-m                 =>   gal/min-ft          4831.17821785317
!      m3/s-W                 =>   (gal/min)/(Btu/h)   4645.27137336702
!      Pa                     =>   ftH2O               0.00033455
!      Pa                     =>   inH2O               0.00401463
!      Pa                     =>   inHg                0.00029613
!      Pa                     =>   Pa                  1
!      W                      =>   W                   1
!      W/(m3/s)               =>   W/(gal/min)         0.0000630902
!      W/m2                   =>   W/m2                1
!      W/m-K                  =>   Btu/h-ft-F          0.577796066000163
!      W/person               =>   W/person            1
!
! Units fields that are not translated
!      $
!      1/hr
!      A
!      A/V
!      Ah
!      Availability
!      Control
!      cycles/hr
!      days
!      deg
!      dimensionless
!      eV
!      hr
!      J/J
!      kg/kg
!      kg-H2O/kg-air
!      kmol
!      kmol/s
!      m3/m3
!      micron
!      minutes
!      Mode
!      ms
!      ohms
!      percent
!      ppm
!      rev/min
!      s
!      V
!      VA
!      W/m2 or deg C
!      W/m2, W or deg C
!      W/s
!      W/W
!      years
! **************************************************************************
"""


# there are 3 kinds of conversions in the TXT file above
# 1. no ip-units -> use 1st
# 2. expected ip-units -> use second
# 3. use the unit as is if it is in the 3rd category

SI: UnitDict = {
    "$/(m3/s)": {"$/(ft3/min)": 0.000472000059660808},
    "$/(W/K)": {"$/(Btu/h-F)": 0.52667614683731},
    "$/kW": {"$/(kBtuh/h)": 0.293083235638921},
    "$/m2": {"$/ft2": 0.0928939733269818},
    "$/m3": {"$/ft3": 0.0283127014102352},
    "(kg/s)/W": {"(lbm/sec)/(Btu/hr)": 0.646078115385742},
    "1/K": {"1/F": 0.555555555555556},
    "1/m": {"1/ft": 0.3048},
    "A/K": {"A/F": 0.555555555555556},
    "C": {"F": ["1.8", "(plus", "32)"], "C": None},
    "cm": {"in": 0.3937},
    "cm2": {"inch2": 0.15500031000062},
    "deltaC": {"deltaF": 1.8},
    "deltaC/hr": {"deltaF/hr": 1.8},
    "deltaJ/kg": {"deltaBtu/lb": 0.0004299},
    "g/GJ": {"lb/MWh": 0.00793664091373665},
    "g/kg": {"grains/lb": 7.0},
    "g/MJ": {"lb/MWh": 7.93664091373665},
    "g/mol": {"lb/mol": 0.0022046},
    "g/m-s": {"lb/ft-s": 0.000671968949659},
    "g/m-s-K": {"lb/ft-s-F": 0.000373574867724868},
    "GJ": {"ton-hrs": 78.9889415481832},
    "J": {"Wh": 0.000277777777777778},
    "J/K": {"Btu/F": 526.565},
    "J/kg": {"Btu/lb": 0.00042986},
    "J/kg-K": {"Btu/lb-F": 0.000239005736137667},
    "J/kg-K2": {"Btu/lb-F2": 0.000132889924714692},
    "J/kg-K3": {"Btu/lb-F3": 7.38277359526066e-05},
    "J/m2-K": {"Btu/ft2-F": 4.89224766847393e-05},
    "J/m3": {"Btu/ft3": 2.68096514745308e-05},
    "J/m3-K": {"Btu/ft3-F": 1.49237004739337e-05},
    "K": {"R": 1.8},
    "K/m": {"F/ft": 0.54861322767449},
    "kg": {"lb": 2.2046},
    "kg/J": {"lb/Btu": 2325.83774250441},
    "kg/kg-K": {"lb/lb-F": 0.555555555555556},
    "kg/m": {"lb/ft": 0.67196893069637},
    "kg/m2": {"lb/ft2": 0.204794053596664},
    "kg/m3": {"lb/ft3": 0.062428},
    "kg/m-s": {"lb/ft-s": 0.67196893069637},
    "kg/m-s-K": {"lb/ft-s-F": 0.373316072609094},
    "kg/m-s-K2": {"lb/ft-s-F2": 0.207397818116164},
    "kg/Pa-s-m2": {"lb/psi-s-ft2": 1412.00523459398},
    "kg/s": {"lb/s": 2.20462247603796},
    "kg/s2": {"lb/s2": 2.2046},
    "kg/s-m": {"lb/s-ft": 0.67196893069637},
    "kJ/kg": {"Btu/lb": 0.429925},
    "kPa": {"psi": 0.145038, "inHg": 0.29523},
    "L/day": {"pint/day": 2.11337629827348},
    "L/GJ": {"gal/kWh": 0.000951022349025202},
    "L/kWh": {"pint/kWh": 2.11337629827348},
    "L/MJ": {"gal/kWh": 0.951022349025202},
    "lux": {"foot-candles": 0.092902267},
    "m": {"ft": 3.28083989501312, "in": 39.3700787401575},
    "m/hr": {"ft/hr": 3.28083989501312},
    "m/s": {"ft/min": 196.850393700787, "miles/hr": 2.2369362920544},
    "m/yr": {"inch/yr": 39.3700787401575},
    "m2": {"ft2": 10.7639104167097},
    "m2/m": {"ft2/ft": 3.28083989501312},
    "m2/person": {"ft2/person": 10.764961},
    "m2/s": {"ft2/s": 10.7639104167097},
    "m2-K/W": {"ft2-F-hr/Btu": 5.678263},
    "m3": {"ft3": 35.3146667214886, "gal": 264.172037284185},
    "m3/GJ": {"ft3/MWh": 127.13292},
    "m3/hr": {"ft3/hr": 35.3146667214886, "gal/hr": 264.172037284185},
    "m3/hr-m2": {"ft3/hr-ft2": 3.28083989501312, "gal/hr-ft2": 24.5423853466941},
    "m3/hr-person": {
        "ft3/hr-person": 35.3146667214886,
        "gal/hr-person": 264.172037284185,
    },
    "m3/kg": {"ft3/lb": 16.018},
    "m3/m2": {"ft3/ft2": 3.28083989501312, "gal/ft2": 24.5423853466941},
    "m3/MJ": {"ft3/kWh": 127.13292},
    "m3/person": {"ft3/person": 35.3146667214886, "gal/person": 264.172037284185},
    "m3/s": {"ft3/min": 2118.88000328931, "gal/min": 15850.3222370511},
    "m3/s-m": {"ft3/min-ft": 645.89, "gal/min-ft": 4831.17821785317},
    "m3/s-m2": {"ft3/min-ft2": 196.85},
    "m3/s-person": {"ft3/min-person": 2118.6438},
    "m3/s-W": {
        "(ft3/min)/(Btu/h)": 621.099127332943,
        "(gal/min)/(Btu/h)": 4645.27137336702,
    },
    "N-m": {"lbf-in": 8.85074900525547},
    "N-s/m2": {"lbf-s/ft2": 0.0208857913669065},
    "Pa": {
        "psi": 0.000145037743897283,
        "ftH2O": 0.00033455,
        "inH2O": 0.00401463,
        "inHg": 0.00029613,
        "Pa": 1.0,
    },
    "percent/K": {"percent/F": 0.555555555555556},
    "person/m2": {"person/ft2": 0.0928939733269818},
    "s/m": {"s/ft": 0.3048},
    "V/K": {"V/F": 0.555555555555556},
    "W": {"Btu/h": 3.4121412858518, "W": 1.0},
    "W/((m3/s)-Pa)": {
        "W/((gal/min)-ftH20)": 0.188582274697355,
        "W/((ft3/min)-inH2O)": 0.117556910599482,
    },
    "W/(m3/s)": {"W/(ft3/min)": 0.0004719475, "W/(gal/min)": 6.30902e-05},
    "W/K": {"Btu/h-F": 1.89563404769544},
    "W/m": {"Btu/h-ft": 1.04072},
    "W/m2": {"Btu/h-ft2": 0.316957210776545, "W/ft2": 0.09290304, "W/m2": 1.0},
    "W/m2-K": {"Btu/h-ft2-F": 0.176110194261872},
    "W/m2-K2": {"Btu/h-ft2-F2": 0.097826},
    "W/m-K": {"Btu-in/h-ft2-F": 6.93481276005548, "Btu/h-ft-F": 0.577796066000163},
    "W/m-K2": {"Btu/h-F2-ft": 0.321418310071648},
    "W/m-K3": {"Btu/h-F3-ft": 0.178565727817582},
    "W/person": {"Btu/h-person": 3.4121412858518, "W/person": 1.0},
    "$": {"$": None},
    "1/hr": {"1/hr": None},
    "A": {"A": None},
    "A/V": {"A/V": None},
    "Ah": {"Ah": None},
    "Availability": {"Availability": None},
    "Control": {"Control": None},
    "cycles/hr": {"cycles/hr": None},
    "days": {"days": None},
    "deg": {"deg": None},
    "dimensionless": {"dimensionless": None},
    "eV": {"eV": None},
    "hr": {"hr": None},
    "J/J": {"J/J": None},
    "kg/kg": {"kg/kg": None},
    "kg-H2O/kg-air": {"kg-H2O/kg-air": None},
    "kmol": {"kmol": None},
    "kmol/s": {"kmol/s": None},
    "m3/m3": {"m3/m3": None},
    "micron": {"micron": None},
    "minutes": {"minutes": None},
    "Mode": {"Mode": None},
    "ms": {"ms": None},
    "ohms": {"ohms": None},
    "percent": {"percent": None},
    "ppm": {"ppm": None},
    "rev/min": {"rev/min": None},
    "s": {"s": None},
    "V": {"V": None},
    "VA": {"VA": None},
    "W/s": {"W/s": None},
    "W/W": {"W/W": None},
    "years": {"years": None},
}


IP: UnitDict = {
    "$/(ft3/min)": {"$/(m3/s)": 0.000472000059660808},
    "$/(Btu/h-F)": {"$/(W/K)": 0.52667614683731},
    "$/(kBtuh/h)": {"$/kW": 0.293083235638921},
    "$/ft2": {"$/m2": 0.0928939733269818},
    "$/ft3": {"$/m3": 0.0283127014102352},
    "(lbm/sec)/(Btu/hr)": {"(kg/s)/W": 0.646078115385742},
    "1/F": {"1/K": 0.555555555555556},
    "1/ft": {"1/m": 0.3048},
    "A/F": {"A/K": 0.555555555555556},
    "F": {"C": ["1.8", "(plus", "32)"]},
    "in": {"cm": 0.3937, "m": 39.3700787401575},
    "inch2": {"cm2": 0.15500031000062},
    "deltaF": {"deltaC": 1.8},
    "deltaF/hr": {"deltaC/hr": 1.8},
    "deltaBtu/lb": {"deltaJ/kg": 0.0004299},
    "lb/MWh": {"g/GJ": 0.00793664091373665, "g/MJ": 7.93664091373665},
    "grains/lb": {"g/kg": 7.0},
    "lb/mol": {"g/mol": 0.0022046},
    "lb/ft-s": {"g/m-s": 0.000671968949659, "kg/m-s": 0.67196893069637},
    "lb/ft-s-F": {"g/m-s-K": 0.000373574867724868, "kg/m-s-K": 0.373316072609094},
    "ton-hrs": {"GJ": 78.9889415481832},
    "Wh": {"J": 0.000277777777777778},
    "Btu/F": {"J/K": 526.565},
    "Btu/lb": {"J/kg": 0.00042986, "kJ/kg": 0.429925},
    "Btu/lb-F": {"J/kg-K": 0.000239005736137667},
    "Btu/lb-F2": {"J/kg-K2": 0.000132889924714692},
    "Btu/lb-F3": {"J/kg-K3": 7.38277359526066e-05},
    "Btu/ft2-F": {"J/m2-K": 4.89224766847393e-05},
    "Btu/ft3": {"J/m3": 2.68096514745308e-05},
    "Btu/ft3-F": {"J/m3-K": 1.49237004739337e-05},
    "R": {"K": 1.8},
    "F/ft": {"K/m": 0.54861322767449},
    "lb": {"kg": 2.2046},
    "lb/Btu": {"kg/J": 2325.83774250441},
    "lb/lb-F": {"kg/kg-K": 0.555555555555556},
    "lb/ft": {"kg/m": 0.67196893069637},
    "lb/ft2": {"kg/m2": 0.204794053596664},
    "lb/ft3": {"kg/m3": 0.062428},
    "lb/ft-s-F2": {"kg/m-s-K2": 0.207397818116164},
    "lb/psi-s-ft2": {"kg/Pa-s-m2": 1412.00523459398},
    "lb/s": {"kg/s": 2.20462247603796},
    "lb/s2": {"kg/s2": 2.2046},
    "lb/s-ft": {"kg/s-m": 0.67196893069637},
    "psi": {"kPa": 0.145038, "Pa": 0.000145037743897283},
    "pint/day": {"L/day": 2.11337629827348},
    "gal/kWh": {"L/GJ": 0.000951022349025202, "L/MJ": 0.951022349025202},
    "pint/kWh": {"L/kWh": 2.11337629827348},
    "foot-candles": {"lux": 0.092902267},
    "ft": {"m": 3.28083989501312},
    "ft/hr": {"m/hr": 3.28083989501312},
    "ft/min": {"m/s": 196.850393700787},
    "miles/hr": {"m/s": 2.2369362920544},
    "inch/yr": {"m/yr": 39.3700787401575},
    "ft2": {"m2": 10.7639104167097},
    "ft2/ft": {"m2/m": 3.28083989501312},
    "ft2/person": {"m2/person": 10.764961},
    "ft2/s": {"m2/s": 10.7639104167097},
    "ft2-F-hr/Btu": {"m2-K/W": 5.678263},
    "ft3": {"m3": 35.3146667214886},
    "gal": {"m3": 264.172037284185},
    "ft3/MWh": {"m3/GJ": 127.13292},
    "ft3/hr": {"m3/hr": 35.3146667214886},
    "ft3/hr-ft2": {"m3/hr-m2": 3.28083989501312},
    "ft3/hr-person": {"m3/hr-person": 35.3146667214886},
    "ft3/lb": {"m3/kg": 16.018},
    "ft3/ft2": {"m3/m2": 3.28083989501312},
    "ft3/kWh": {"m3/MJ": 127.13292},
    "ft3/person": {"m3/person": 35.3146667214886},
    "ft3/min": {"m3/s": 2118.88000328931},
    "ft3/min-ft": {"m3/s-m": 645.89},
    "ft3/min-ft2": {"m3/s-m2": 196.85},
    "ft3/min-person": {"m3/s-person": 2118.6438},
    "(ft3/min)/(Btu/h)": {"m3/s-W": 621.099127332943},
    "lbf-in": {"N-m": 8.85074900525547},
    "lbf-s/ft2": {"N-s/m2": 0.0208857913669065},
    "percent/F": {"percent/K": 0.555555555555556},
    "person/ft2": {"person/m2": 0.0928939733269818},
    "s/ft": {"s/m": 0.3048},
    "V/F": {"V/K": 0.555555555555556},
    "Btu/h": {"W": 3.4121412858518},
    "W/((gal/min)-ftH20)": {"W/((m3/s)-Pa)": 0.188582274697355},
    "W/((ft3/min)-inH2O)": {"W/((m3/s)-Pa)": 0.117556910599482},
    "W/(ft3/min)": {"W/(m3/s)": 0.0004719475},
    "Btu/h-F": {"W/K": 1.89563404769544},
    "Btu/h-ft": {"W/m": 1.04072},
    "Btu/h-ft2": {"W/m2": 0.316957210776545},
    "W/ft2": {"W/m2": 0.09290304},
    "Btu/h-ft2-F": {"W/m2-K": 0.176110194261872},
    "Btu/h-ft2-F2": {"W/m2-K2": 0.097826},
    "Btu-in/h-ft2-F": {"W/m-K": 6.93481276005548},
    "Btu/h-F2-ft": {"W/m-K2": 0.321418310071648},
    "Btu/h-F3-ft": {"W/m-K3": 0.178565727817582},
    "Btu/h-person": {"W/person": 3.4121412858518},
    "inHg": {"kPa": 0.29523, "Pa": 0.00029613},
    "gal/hr": {"m3/hr": 264.172037284185},
    "gal/hr-ft2": {"m3/hr-m2": 24.5423853466941},
    "gal/hr-person": {"m3/hr-person": 264.172037284185},
    "gal/ft2": {"m3/m2": 24.5423853466941},
    "gal/person": {"m3/person": 264.172037284185},
    "gal/min": {"m3/s": 15850.3222370511},
    "gal/min-ft": {"m3/s-m": 4831.17821785317},
    "(gal/min)/(Btu/h)": {"m3/s-W": 4645.27137336702},
    "ftH2O": {"Pa": 0.00033455},
    "inH2O": {"Pa": 0.00401463},
    "Pa": {"Pa": 1.0},
    "W": {"W": 1.0},
    "W/(gal/min)": {"W/(m3/s)": 6.30902e-05},
    "W/m2": {"W/m2": 1.0},
    "Btu/h-ft-F": {"W/m-K": 0.577796066000163},
    "W/person": {"W/person": 1.0},
    "$": {"$": None},
    "1/hr": {"1/hr": None},
    "A": {"A": None},
    "A/V": {"A/V": None},
    "Ah": {"Ah": None},
    "Availability": {"Availability": None},
    "Control": {"Control": None},
    "cycles/hr": {"cycles/hr": None},
    "days": {"days": None},
    "deg": {"deg": None},
    "dimensionless": {"dimensionless": None},
    "eV": {"eV": None},
    "hr": {"hr": None},
    "J/J": {"J/J": None},
    "kg/kg": {"kg/kg": None},
    "kg-H2O/kg-air": {"kg-H2O/kg-air": None},
    "kmol": {"kmol": None},
    "kmol/s": {"kmol/s": None},
    "m3/m3": {"m3/m3": None},
    "micron": {"micron": None},
    "minutes": {"minutes": None},
    "Mode": {"Mode": None},
    "ms": {"ms": None},
    "ohms": {"ohms": None},
    "percent": {"percent": None},
    "ppm": {"ppm": None},
    "rev/min": {"rev/min": None},
    "s": {"s": None},
    "V": {"V": None},
    "VA": {"VA": None},
    "C": {"C": None},
    "W/s": {"W/s": None},
    "W/W": {"W/W": None},
    "years": {"years": None},
}

SI_DEFAULT: dict[str, str] = {
    "$/(m3/s)": "$/(ft3/min)",
    "$/(W/K)": "$/(Btu/h-F)",
    "$/kW": "$/(kBtuh/h)",
    "$/m2": "$/ft2",
    "$/m3": "$/ft3",
    "(kg/s)/W": "(lbm/sec)/(Btu/hr)",
    "1/K": "1/F",
    "1/m": "1/ft",
    "A/K": "A/F",
    "C": "F",
    "cm": "in",
    "cm2": "inch2",
    "deltaC": "deltaF",
    "deltaC/hr": "deltaF/hr",
    "deltaJ/kg": "deltaBtu/lb",
    "g/GJ": "lb/MWh",
    "g/kg": "grains/lb",
    "g/MJ": "lb/MWh",
    "g/mol": "lb/mol",
    "g/m-s": "lb/ft-s",
    "g/m-s-K": "lb/ft-s-F",
    "GJ": "ton-hrs",
    "J": "Wh",
    "J/K": "Btu/F",
    "J/kg": "Btu/lb",
    "J/kg-K": "Btu/lb-F",
    "J/kg-K2": "Btu/lb-F2",
    "J/kg-K3": "Btu/lb-F3",
    "J/m2-K": "Btu/ft2-F",
    "J/m3": "Btu/ft3",
    "J/m3-K": "Btu/ft3-F",
    "K": "R",
    "K/m": "F/ft",
    "kg": "lb",
    "kg/J": "lb/Btu",
    "kg/kg-K": "lb/lb-F",
    "kg/m": "lb/ft",
    "kg/m2": "lb/ft2",
    "kg/m3": "lb/ft3",
    "kg/m-s": "lb/ft-s",
    "kg/m-s-K": "lb/ft-s-F",
    "kg/m-s-K2": "lb/ft-s-F2",
    "kg/Pa-s-m2": "lb/psi-s-ft2",
    "kg/s": "lb/s",
    "kg/s2": "lb/s2",
    "kg/s-m": "lb/s-ft",
    "kJ/kg": "Btu/lb",
    "kPa": "psi",
    "L/day": "pint/day",
    "L/GJ": "gal/kWh",
    "L/kWh": "pint/kWh",
    "L/MJ": "gal/kWh",
    "lux": "foot-candles",
    "m": "ft",
    "m/hr": "ft/hr",
    "m/s": "ft/min",
    "m/yr": "inch/yr",
    "m2": "ft2",
    "m2/m": "ft2/ft",
    "m2/person": "ft2/person",
    "m2/s": "ft2/s",
    "m2-K/W": "ft2-F-hr/Btu",
    "m3": "ft3",
    "m3/GJ": "ft3/MWh",
    "m3/hr": "ft3/hr",
    "m3/hr-m2": "ft3/hr-ft2",
    "m3/hr-person": "ft3/hr-person",
    "m3/kg": "ft3/lb",
    "m3/m2": "ft3/ft2",
    "m3/MJ": "ft3/kWh",
    "m3/person": "ft3/person",
    "m3/s": "ft3/min",
    "m3/s-m": "ft3/min-ft",
    "m3/s-m2": "ft3/min-ft2",
    "m3/s-person": "ft3/min-person",
    "m3/s-W": "(ft3/min)/(Btu/h)",
    "N-m": "lbf-in",
    "N-s/m2": "lbf-s/ft2",
    "Pa": "psi",
    "percent/K": "percent/F",
    "person/m2": "person/ft2",
    "s/m": "s/ft",
    "V/K": "V/F",
    "W": "Btu/h",
    "W/((m3/s)-Pa)": "W/((gal/min)-ftH20)",
    "W/(m3/s)": "W/(ft3/min)",
    "W/K": "Btu/h-F",
    "W/m": "Btu/h-ft",
    "W/m2": "Btu/h-ft2",
    "W/m2-K": "Btu/h-ft2-F",
    "W/m2-K2": "Btu/h-ft2-F2",
    "W/m-K": "Btu-in/h-ft2-F",
    "W/m-K2": "Btu/h-F2-ft",
    "W/m-K3": "Btu/h-F3-ft",
    "W/person": "Btu/h-person",
    "$": "$",
    "1/hr": "1/hr",
    "A": "A",
    "A/V": "A/V",
    "Ah": "Ah",
    "Availability": "Availability",
    "Control": "Control",
    "cycles/hr": "cycles/hr",
    "days": "days",
    "deg": "deg",
    "dimensionless": "dimensionless",
    "eV": "eV",
    "hr": "hr",
    "J/J": "J/J",
    "kg/kg": "kg/kg",
    "kg-H2O/kg-air": "kg-H2O/kg-air",
    "kmol": "kmol",
    "kmol/s": "kmol/s",
    "m3/m3": "m3/m3",
    "micron": "micron",
    "minutes": "minutes",
    "Mode": "Mode",
    "ms": "ms",
    "ohms": "ohms",
    "percent": "percent",
    "ppm": "ppm",
    "rev/min": "rev/min",
    "s": "s",
    "V": "V",
    "VA": "VA",
    "W/s": "W/s",
    "W/W": "W/W",
    "years": "years",
}

IP_DEFAULT: dict[str, str] = {
    "$/(ft3/min)": "$/(m3/s)",
    "$/(Btu/h-F)": "$/(W/K)",
    "$/(kBtuh/h)": "$/kW",
    "$/ft2": "$/m2",
    "$/ft3": "$/m3",
    "(lbm/sec)/(Btu/hr)": "(kg/s)/W",
    "1/F": "1/K",
    "1/ft": "1/m",
    "A/F": "A/K",
    "F": "C",
    "in": "cm",
    "inch2": "cm2",
    "deltaF": "deltaC",
    "deltaF/hr": "deltaC/hr",
    "deltaBtu/lb": "deltaJ/kg",
    "lb/MWh": "g/GJ",
    "grains/lb": "g/kg",
    "lb/mol": "g/mol",
    "lb/ft-s": "g/m-s",
    "lb/ft-s-F": "g/m-s-K",
    "ton-hrs": "GJ",
    "Wh": "J",
    "Btu/F": "J/K",
    "Btu/lb": "J/kg",
    "Btu/lb-F": "J/kg-K",
    "Btu/lb-F2": "J/kg-K2",
    "Btu/lb-F3": "J/kg-K3",
    "Btu/ft2-F": "J/m2-K",
    "Btu/ft3": "J/m3",
    "Btu/ft3-F": "J/m3-K",
    "R": "K",
    "F/ft": "K/m",
    "lb": "kg",
    "lb/Btu": "kg/J",
    "lb/lb-F": "kg/kg-K",
    "lb/ft": "kg/m",
    "lb/ft2": "kg/m2",
    "lb/ft3": "kg/m3",
    "lb/ft-s-F2": "kg/m-s-K2",
    "lb/psi-s-ft2": "kg/Pa-s-m2",
    "lb/s": "kg/s",
    "lb/s2": "kg/s2",
    "lb/s-ft": "kg/s-m",
    "psi": "kPa",
    "pint/day": "L/day",
    "gal/kWh": "L/GJ",
    "pint/kWh": "L/kWh",
    "foot-candles": "lux",
    "ft": "m",
    "ft/hr": "m/hr",
    "ft/min": "m/s",
    "miles/hr": "m/s",
    "inch/yr": "m/yr",
    "ft2": "m2",
    "ft2/ft": "m2/m",
    "ft2/person": "m2/person",
    "ft2/s": "m2/s",
    "ft2-F-hr/Btu": "m2-K/W",
    "ft3": "m3",
    "gal": "m3",
    "ft3/MWh": "m3/GJ",
    "ft3/hr": "m3/hr",
    "ft3/hr-ft2": "m3/hr-m2",
    "ft3/hr-person": "m3/hr-person",
    "ft3/lb": "m3/kg",
    "ft3/ft2": "m3/m2",
    "ft3/kWh": "m3/MJ",
    "ft3/person": "m3/person",
    "ft3/min": "m3/s",
    "ft3/min-ft": "m3/s-m",
    "ft3/min-ft2": "m3/s-m2",
    "ft3/min-person": "m3/s-person",
    "(ft3/min)/(Btu/h)": "m3/s-W",
    "lbf-in": "N-m",
    "lbf-s/ft2": "N-s/m2",
    "percent/F": "percent/K",
    "person/ft2": "person/m2",
    "s/ft": "s/m",
    "V/F": "V/K",
    "Btu/h": "W",
    "W/((gal/min)-ftH20)": "W/((m3/s)-Pa)",
    "W/((ft3/min)-inH2O)": "W/((m3/s)-Pa)",
    "W/(ft3/min)": "W/(m3/s)",
    "Btu/h-F": "W/K",
    "Btu/h-ft": "W/m",
    "Btu/h-ft2": "W/m2",
    "W/ft2": "W/m2",
    "Btu/h-ft2-F": "W/m2-K",
    "Btu/h-ft2-F2": "W/m2-K2",
    "Btu-in/h-ft2-F": "W/m-K",
    "Btu/h-F2-ft": "W/m-K2",
    "Btu/h-F3-ft": "W/m-K3",
    "Btu/h-person": "W/person",
    "inHg": "kPa",
    "gal/hr": "m3/hr",
    "gal/hr-ft2": "m3/hr-m2",
    "gal/hr-person": "m3/hr-person",
    "gal/ft2": "m3/m2",
    "gal/person": "m3/person",
    "gal/min": "m3/s",
    "gal/min-ft": "m3/s-m",
    "(gal/min)/(Btu/h)": "m3/s-W",
    "ftH2O": "Pa",
    "inH2O": "Pa",
    "Pa": "Pa",
    "W": "W",
    "W/(gal/min)": "W/(m3/s)",
    "W/m2": "W/m2",
    "Btu/h-ft-F": "W/m-K",
    "W/person": "W/person",
    "$": "$",
    "1/hr": "1/hr",
    "A": "A",
    "A/V": "A/V",
    "Ah": "Ah",
    "Availability": "Availability",
    "Control": "Control",
    "cycles/hr": "cycles/hr",
    "days": "days",
    "deg": "deg",
    "dimensionless": "dimensionless",
    "eV": "eV",
    "hr": "hr",
    "J/J": "J/J",
    "kg/kg": "kg/kg",
    "kg-H2O/kg-air": "kg-H2O/kg-air",
    "kmol": "kmol",
    "kmol/s": "kmol/s",
    "m3/m3": "m3/m3",
    "micron": "micron",
    "minutes": "minutes",
    "Mode": "Mode",
    "ms": "ms",
    "ohms": "ohms",
    "percent": "percent",
    "ppm": "ppm",
    "rev/min": "rev/min",
    "s": "s",
    "V": "V",
    "VA": "VA",
    "C": "C",
    "W/s": "W/s",
    "W/W": "W/W",
    "years": "years",
}


def getconversions(
    txt: Optional[str] = None,
) -> tuple[UnitDict, UnitDict, Dict[str, str], Dict[str, str]]:
    """
    create the conversion data structure for this library

    This function generates the values in the constants SI, IP, SI_DEFAULT and IP_DEFAULT. Ulikely that you will ever neeed to use this function. It was used to build up this module

    :param txt: the raw text from the IDD which contains the conversion factors
    :returns SI: The value of the SI constant
    :returns IP: The value of the IP constant
    :returns SI_DEFAULT: The value of the SI_DEFAULT
    :returns IP_DEFAULT: The value of the IP_DEFAULT
    """
    if not txt:
        txt = TXT
    msp = txt.split("!\n")
    c1 = msp[0].splitlines()
    c1.pop(0)

    si: Dict[str, Any] = dict()
    ip: Dict[str, Any] = dict()

    for c in c1:
        cc = c.split()
        cc.pop(0)
        cc.pop(1)
        try:
            si.setdefault(cc[0], []).append((cc[1], float(cc[-1])))
            ip.setdefault(cc[1], []).append((cc[0], float(cc[-1])))
        except ValueError:
            si.setdefault(cc[0], []).append((cc[1], cc[2:]))
            ip.setdefault(cc[1], []).append((cc[0], cc[2:]))
    c1 = msp[2].splitlines()
    for c in c1:
        cc = c.split()
        cc.pop(0)
        cc.pop(1)
        try:
            si.setdefault(cc[0], []).append((cc[1], float(cc[-1])))
            ip.setdefault(cc[1], []).append((cc[0], float(cc[-1])))
        except ValueError:
            si.setdefault(cc[0], []).append((cc[1], cc[2:]))
            ip.setdefault(cc[1], []).append((cc[0], cc[2:]))
    c2 = msp[3].splitlines()
    c2.pop(0)
    c2.pop(-1)
    for c in [c.split()[-1] for c in c2]:
        si.setdefault(c, []).append((c, None))
        ip.setdefault(c, []).append((c, None))
    ssi, iip = _setdefaultindct(si), _setdefaultindct(ip)
    return (
        _remove_defaultkey(ssi),  # SI
        _remove_defaultkey(iip),  # IP
        {k: str(v) for k, v in _getdefaultkey(ssi).items()},  # SI_DEFAULT
        {k: str(v) for k, v in _getdefaultkey(iip).items()},  # IP_DEFAULT
    )


def _setdefaultindct(dct: Dict[str, Any]) -> UnitDict:
    """
    Sets a default value to be used internally by 'getconversions`

    """
    newdct = {}
    for key in dct:
        d = dict(defaultkey=dct[key][0][0])
        d.update(dict(dct[key]))
        newdct[key] = d
    return newdct


def convert2ip(
    val: float,
    siunit: str,
    ipunit: Optional[str] = None,
    unitstr: bool = True,
    wrapin: Optional[str] = None,
) -> Union[float, tuple[float, str]]:
    """
    convert val from si units to ip units

    the conversion will be done to the default ip unit. if you have a specific ip unit you want to convert to, give it's value to the `ipunit` parameter

    By default, the function will also return the ip unit string. to return only the ip value, set `unitstr=False`. You can wrap the unit string by setting a value to wrapin='[X]' where X is replaced by the unit string. '['  and ']' can be any string

    Sample code::

        epconversions.convert2ip(4, 'm')
        >> (13.12335958005248, 'ft')
        epconversions.convert2ip(4, 'm', 'in')
        >> (157.48031496063, 'in')
        epconversions.convert2ip(4, 'm', 'in', unitstr=None)
        >> 157.48031496063
        epconversions.convert2ip(4, 'm', 'in', wrapin='[X]')
        >> (157.48031496063, '[in]')
        epconversions.convert2ip(4, 'm', 'in', wrapin='unit = [X]')
        >> (157.48031496063, 'unit = [in]')



    :param val: a numeric value
    :param siunit: the unit for the value (kg, m, etc.)
    :param ipunit: if you know the ip unit you want returned. Else it will use the default unit
    :param unitstr: True if you want the unit string returned
    :param wrapin: wrap the init string in this.
    :returns new_val: The new converted value
    :returns ustr: returns unit string if unitstr=True

    """
    # calculates the new value
    # get conversion factor
    conv: Optional[Union[str, float, None, list[str]]]
    if not siunit:
        conv = 1.0
    elif siunit not in SI:
        conv = 1.0
    elif not ipunit:
        default = SI_DEFAULT[siunit]
        conv = SI[siunit][default]
    else:
        conv = SI[siunit][ipunit]

    # do conversion
    new_val = _doconversion(val, conv)

    # make the unit string
    ustr = ""
    if unitstr:
        if not siunit:
            ustr = ""
        elif siunit not in SI:
            ustr = siunit
        elif ipunit:
            ustr = ipunit
        else:
            ustr = default
        # wrap the unitstr
        if not wrapin:
            wrapin = "X"
        elif ustr:
            ustr = wrapin.replace("X", ustr)
        else:
            pass

    # return the results
    if unitstr:
        return new_val, ustr
    else:
        return new_val


def convert2si(
    val: float,
    ipunit: str,
    siunit: Optional[str] = None,
    unitstr: bool = True,
    wrapin: Optional[str] = None,
) -> Union[float, tuple[float, str]]:
    """
    convert val from ip units to si units

    the conversion will be done to the default si unit. if you have a specific si unit you want to convert to, give it's value to the `siunit` parameter

    By default, the function will also return the si unit string. to return only the si value, set `unitstr=False`. You can wrap the unit string by setting a value to wrapin='[X]' where X is replaced by the unit string. '['  and ']' can be any string

    Sample code::

        epconversions.convert2si(5, 'in')
        >> (12.700025400050801, 'cm')
        epconversions.convert2si(5, 'in', 'm')
        >> (0.12699999999999992, 'm')
        epconversions.convert2si(5, 'in', 'm', unitstr=False)
        >> 0.12699999999999992
        epconversions.convert2si(5, 'in', 'm', wrapin='[X]')
        >> (0.12699999999999992, '[m]')
        epconversions.convert2si(5, 'in', 'm', wrapin='unit = [X]')
        >>  wrapin='unit = [X]')


    :param val: a numeric value
    :param ipunit: the unit for the value (ft, in, F etc.)
    :param siunit: if you know the si unit you want returned. Else it will use the default unit
    :param unitstr: True if you want the unit string returned
    :param wrapin: wrap the init string in this.
    :returns new_val: The new converted value
    :returns ustr: returns unit string if unitstr=True

    """
    # calculates the new value
    # get conversion factor
    #     conv: Optional[Union[str, float, None, list[str]]]
    conv: UnitDictValVal
    if not ipunit:
        conv = 1.0
    elif ipunit not in IP:
        conv = 1.0
    elif not siunit:
        default = IP_DEFAULT[ipunit]
        conv = IP[ipunit][default]
    else:
        conv = IP[ipunit][siunit]

    # do conversion
    new_val = _doconversion(val, conv, reverse=True)

    # make the unit string
    ustr = ""
    if unitstr:
        if not ipunit:
            ustr = ""
        elif ipunit not in IP:
            ustr = ipunit
        elif siunit:
            ustr = siunit
        else:
            ustr = default
        # wrap the unitstr
        if not wrapin:
            wrapin = "X"
        elif ustr:
            ustr = wrapin.replace("X", ustr)
        else:
            pass

    # return the results
    if unitstr:
        return new_val, ustr
    else:
        return new_val


def _doconversion(
    val: float,
    conv: Optional[Union[str, float, None, list[str]]],
    reverse: bool = False,
) -> float:
    """does the conversions

    :param val: val is converted
    :param conv: this is the conversion factor or rule
    :param reverse: if True, use 1/conv or reverse of the rule
    :returns new_value: the converted value
    """
    try:
        val = float(val)
    except (ValueError, TypeError) as e:
        pass
    if reverse:
        try:
            conv = 1 / conv  # type: ignore
        except TypeError:
            pass
    try:
        if conv == ["1.8", "(plus", "32)"]:
            if reverse:
                new_val = (val - 32) / 1.8
            else:
                new_val = (val * 1.8) + 32
        else:
            new_val = val * conv  # type: ignore
    except TypeError:
        new_val = val
    return new_val


def allsiunits() -> list[str]:
    """return a list of all SI units that this module can convert

    :returns siunits: a list of all si units
    """
    return list(SI.keys())


def allipunits() -> list[str]:
    """return a list of all the IP units that this module can convert

    :returns ipunits: a list of all ip units
    """
    return list(IP.keys())


def getipunits(siunit: str, si: Optional[UnitDict] = None) -> set[str]:
    """return all the ip units avaliable for this si unit

    :param siunit: si unit
    :param si: Use this in case you want to override the default constant SI
    :returns ipunits: all the ip units avaliable for this si unit
    """
    if not si:
        si = SI
    dct = dict(si[siunit])
    return set(dct.keys())


def getsiunits(ipunit: str, ip: Optional[UnitDict] = None) -> set[str]:
    """return all the si units avaliable for this ip unit

    :param ipunit: ip unit
    :param ip: Use this in case you want to override the default constant IP
    :returns siunts: all the si units avaliable for this ip unit
    """
    if not ip:
        ip = IP
    dct = dict(ip[ipunit])
    return set(dct.keys())


def _remove_defaultkey(a: UnitDict) -> UnitDict:
    """for internal use"""
    return {k: {kk: a[k][kk] for kk in a[k] if kk != "defaultkey"} for k in a}


def _getdefaultkey(a: UnitDict) -> UnitDictVal:
    """for internal use by getconversions"""
    return {k: a[k]["defaultkey"] for k in a}


def defaultsiunit(ipunit: str) -> str:
    """get the default `si unit` for the given `ip unit`

    :param ipunit: ip unit
    :returns siunit: the default `si unit` for the given `ip unit`
    """
    return IP_DEFAULT[ipunit]


def defaultipunit(siunit: str) -> str:
    """get the default `ip unit` for the given `si unit`

    :param siunit: si unit
    :returns ipunit: the default `ip unit` for the given `si unit`
    """
    return SI_DEFAULT[siunit]
