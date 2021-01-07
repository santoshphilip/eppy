# Copyright (c) 2020 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-
"""py.test for fasthtml"""


from io import StringIO
from pathlib import Path
import pytest
from eppy.results import readhtml
from eppy.results import fasthtml


class SampleHtml(object):
    """Sample html text"""

    def __init__(self):
        self.html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN""http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title> California DGS- 10th & O Street Offices 2 SACRAMENTO-EXECUTIVE_724830_CZ2010 ** SACRAMENTO-EXECUTIVE-AP - USA Custom-724830 WMO#=724830
  2019-08-19
  10:51:57
 - EnergyPlus</title>
</head>
<body>
<p><a href="#toc" style="float: right">Table of Contents</a></p>
<a name=top></a>
<p>Program Version:<b>EnergyPlus, Version 8.5.0-c87e61b44b, YMD=2019.08.19 10:39</b></p>
<p>Tabular Output Report in Format: <b>HTML</b></p>
<p>Building: <b>California DGS- 10th & O Street Offices 2</b></p>
<p>Environment: <b>SACRAMENTO-EXECUTIVE_724830_CZ2010 ** SACRAMENTO-EXECUTIVE-AP - USA Custom-724830 WMO#=724830</b></p>
<p>Simulation Timestamp: <b>2019-08-19
  10:51:57</b></p>
<hr>
<p><a href="#toc" style="float: right">Table of Contents</a></p>
<a name=AnnualBuildingUtilityPerformanceSummary::EntireFacility></a>
<p>Report:<b> Annual Building Utility Performance Summary</b></p>
<p>For:<b> Entire Facility</b></p>
<p>Timestamp: <b>2019-08-19
    10:51:57</b></p>
<b>Values gathered over      8760.00 hours</b><br><br>
<b></b><br><br>
<b>Site and Source Energy</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Site and Source Energy-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Total Energy [kBtu]</td>
    <td align="right">Energy Per Total Building Area [kBtu/ft2]</td>
    <td align="right">Energy Per Conditioned Building Area [kBtu/ft2]</td>
  </tr>
  <tr>
    <td align="right">Total Site Energy</td>
    <td align="right"> 12372300.67</td>
    <td align="right">       27.07</td>
    <td align="right">       28.11</td>
  </tr>
  <tr>
    <td align="right">Net Site Energy</td>
    <td align="right"> 12372300.67</td>
    <td align="right">       27.07</td>
    <td align="right">       28.11</td>
  </tr>
  <tr>
    <td align="right">Total Source Energy</td>
    <td align="right"> 31924186.59</td>
    <td align="right">       69.85</td>
    <td align="right">       72.53</td>
  </tr>
  <tr>
    <td align="right">Net Source Energy</td>
    <td align="right"> 31924186.59</td>
    <td align="right">       69.85</td>
    <td align="right">       72.53</td>
  </tr>
</table>
<br><br>
<b>Site to Source Energy Conversion Factors</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Site to Source Energy Conversion Factors-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Site=>Source Conversion Factor</td>
  </tr>
  <tr>
    <td align="right">Electricity</td>
    <td align="right">       3.167</td>
  </tr>
  <tr>
    <td align="right">Natural Gas</td>
    <td align="right">       1.084</td>
  </tr>
  <tr>
    <td align="right">District Cooling</td>
    <td align="right">       1.056</td>
  </tr>
  <tr>
    <td align="right">District Heating</td>
    <td align="right">       3.613</td>
  </tr>
  <tr>
    <td align="right">Steam</td>
    <td align="right">       0.300</td>
  </tr>
  <tr>
    <td align="right">Gasoline</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Diesel</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Coal</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Fuel Oil #1</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Fuel Oil #2</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Propane</td>
    <td align="right">       1.050</td>
  </tr>
  <tr>
    <td align="right">Other Fuel 1</td>
    <td align="right">       1.000</td>
  </tr>
  <tr>
    <td align="right">Other Fuel 2</td>
    <td align="right">       1.000</td>
  </tr>
</table>
<br><br>
<b>Building Area</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Building Area-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Area [ft2]</td>
  </tr>
  <tr>
    <td align="right">Total Building Area</td>
    <td align="right">   457021.76</td>
  </tr>
  <tr>
    <td align="right">Net Conditioned Building Area</td>
    <td align="right">   440178.05</td>
  </tr>
  <tr>
    <td align="right">Unconditioned Building Area</td>
    <td align="right">    16843.71</td>
  </tr>
</table>
<br><br>
<b>End Uses</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_End Uses-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Electricity [kBtu]</td>
    <td align="right">Natural Gas [kBtu]</td>
    <td align="right">Additional Fuel [kBtu]</td>
    <td align="right">District Cooling [kBtu]</td>
    <td align="right">District Heating [kBtu]</td>
    <td align="right">Water [gal]</td>
  </tr>
  <tr>
    <td align="right">Heating</td>
    <td align="right">      699.76</td>
    <td align="right">  3484218.01</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Cooling</td>
    <td align="right">   778887.08</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Interior Lighting</td>
    <td align="right">  1451508.91</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Exterior Lighting</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Interior Equipment</td>
    <td align="right">  5243267.78</td>
    <td align="right">      606.58</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Exterior Equipment</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Fans</td>
    <td align="right">  1011588.31</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Pumps</td>
    <td align="right">   308846.84</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Heat Rejection</td>
    <td align="right">    92677.39</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">  1370313.32</td>
  </tr>
  <tr>
    <td align="right">Humidification</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Heat Recovery</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Water Systems</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Refrigeration</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Generators</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Total End Uses</td>
    <td align="right">  8887476.08</td>
    <td align="right">  3484824.60</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">  1370313.32</td>
  </tr>
</table>
<i>Note: Natural gas appears to be the principal heating source based on energy usage.</i>
<br><br>
<b>End Uses By Subcategory</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_End Uses By Subcategory-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Subcategory</td>
    <td align="right">Electricity [kBtu]</td>
    <td align="right">Natural Gas [kBtu]</td>
    <td align="right">Additional Fuel [kBtu]</td>
    <td align="right">District Cooling [kBtu]</td>
    <td align="right">District Heating [kBtu]</td>
    <td align="right">Water [gal]</td>
  </tr>
  <tr>
    <td align="right">Heating</td>
    <td align="right">Boiler</td>
    <td align="right">        0.00</td>
    <td align="right">  3484218.01</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">Boiler Parasitic</td>
    <td align="right">      699.76</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Cooling</td>
    <td align="right">General</td>
    <td align="right">   778887.08</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Interior Lighting</td>
    <td align="right">ComplianceLtg</td>
    <td align="right">  1355763.53</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">NonComplianceLtg</td>
    <td align="right">    95745.38</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Exterior Lighting</td>
    <td align="right">General</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Interior Equipment</td>
    <td align="right">Receptacle</td>
    <td align="right">  4832413.78</td>
    <td align="right">      606.58</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">Process</td>
    <td align="right">    59134.94</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">Internal Transport</td>
    <td align="right">   351719.06</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Exterior Equipment</td>
    <td align="right">General</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Fans</td>
    <td align="right">General</td>
    <td align="right">   955401.72</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">ProcessMotors</td>
    <td align="right">    56186.59</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Pumps</td>
    <td align="right">General</td>
    <td align="right">   308846.84</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Heat Rejection</td>
    <td align="right">General</td>
    <td align="right">    92677.39</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">  1370313.32</td>
  </tr>
  <tr>
    <td align="right">Humidification</td>
    <td align="right">General</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Heat Recovery</td>
    <td align="right">General</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Water Systems</td>
    <td align="right">General</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Refrigeration</td>
    <td align="right">General</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Generators</td>
    <td align="right">General</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
</table>
<br><br>
<b>Normalized Metrics</b><br><br>
<b>Utility Use Per Conditioned Floor Area</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Utility Use Per Conditioned Floor Area-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Electricity Intensity [kBtu/ft2]</td>
    <td align="right">Natural Gas Intensity [kBtu/ft2]</td>
    <td align="right">Additional Fuel Intensity [kBtu/ft2]</td>
    <td align="right">District Cooling Intensity [kBtu/ft2]</td>
    <td align="right">District Heating Intensity [kBtu/ft2]</td>
    <td align="right">Water Intensity [gal/ft2]</td>
  </tr>
  <tr>
    <td align="right">Lighting</td>
    <td align="right">        3.30</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">HVAC</td>
    <td align="right">        4.98</td>
    <td align="right">        7.92</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        3.11</td>
  </tr>
  <tr>
    <td align="right">Other</td>
    <td align="right">       11.91</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Total</td>
    <td align="right">       20.19</td>
    <td align="right">        7.92</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        3.11</td>
  </tr>
</table>
<br><br>
<b>Utility Use Per Total Floor Area</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Utility Use Per Total Floor Area-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Electricity Intensity [kBtu/ft2]</td>
    <td align="right">Natural Gas Intensity [kBtu/ft2]</td>
    <td align="right">Additional Fuel Intensity [kBtu/ft2]</td>
    <td align="right">District Cooling Intensity [kBtu/ft2]</td>
    <td align="right">District Heating Intensity [kBtu/ft2]</td>
    <td align="right">Water Intensity [gal/ft2]</td>
  </tr>
  <tr>
    <td align="right">Lighting</td>
    <td align="right">        3.18</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">HVAC</td>
    <td align="right">        4.80</td>
    <td align="right">        7.62</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        3.00</td>
  </tr>
  <tr>
    <td align="right">Other</td>
    <td align="right">       11.47</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Total</td>
    <td align="right">       19.45</td>
    <td align="right">        7.63</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
    <td align="right">        3.00</td>
  </tr>
</table>
<br><br>
<b>Electric Loads Satisfied</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Electric Loads Satisfied-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Electricity [kBtu]</td>
    <td align="right">Percent Electricity [%]</td>
  </tr>
  <tr>
    <td align="right">Fuel-Fired Power Generation</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">High Temperature Geothermal*</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Photovoltaic Power</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Wind Power</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Power Conversion</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Net Decrease in On-Site Storage</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Total On-Site Electric Sources</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Electricity Coming From Utility</td>
    <td align="right"> 8887476.075</td>
    <td align="right">      100.00</td>
  </tr>
  <tr>
    <td align="right">Surplus Electricity Going To Utility</td>
    <td align="right">       0.000</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Net Electricity From Utility</td>
    <td align="right"> 8887476.075</td>
    <td align="right">      100.00</td>
  </tr>
  <tr>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Total On-Site and Utility Electric Sources</td>
    <td align="right"> 8887476.075</td>
    <td align="right">      100.00</td>
  </tr>
  <tr>
    <td align="right">Total Electricity End Uses</td>
    <td align="right"> 8887476.075</td>
    <td align="right">      100.00</td>
  </tr>
</table>
<br><br>
<b>On-Site Thermal Sources</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_On-Site Thermal Sources-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Heat [kBtu]</td>
    <td align="right">Percent Heat [%]</td>
  </tr>
  <tr>
    <td align="right">Water-Side Heat Recovery</td>
    <td align="right">        0.00</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Air to Air Heat Recovery for Cooling</td>
    <td align="right">        0.00</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Air to Air Heat Recovery for Heating</td>
    <td align="right">        0.00</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">High-Temperature Geothermal*</td>
    <td align="right">        0.00</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Solar Water Thermal</td>
    <td align="right">        0.00</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Solar Air Thermal</td>
    <td align="right">        0.00</td>
    <td align="right">&nbsp;</td>
  </tr>
  <tr>
    <td align="right">Total On-Site Thermal Sources</td>
    <td align="right">        0.00</td>
    <td align="right">&nbsp;</td>
  </tr>
</table>
<br><br>
<b>Water Source Summary</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Water Source Summary-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Water [gal]</td>
    <td align="right">Percent Water [%]</td>
  </tr>
  <tr>
    <td align="right">Rainwater Collection</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Condensate Collection</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Groundwater Well</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Total On Site Water Sources</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">-</td>
    <td align="right">-</td>
    <td align="right">-</td>
  </tr>
  <tr>
    <td align="right">Initial Storage</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Final Storage</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Change in Storage</td>
    <td align="right">        0.00</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">-</td>
    <td align="right">-</td>
    <td align="right">-</td>
  </tr>
  <tr>
    <td align="right">Water Supplied by Utility</td>
    <td align="right">  1370313.32</td>
    <td align="right">      100.00</td>
  </tr>
  <tr>
    <td align="right">-</td>
    <td align="right">-</td>
    <td align="right">-</td>
  </tr>
  <tr>
    <td align="right">Total On Site, Change in Storage, and Utility Water Sources</td>
    <td align="right">  1370313.32</td>
    <td align="right">      100.00</td>
  </tr>
  <tr>
    <td align="right">Total Water End Uses</td>
    <td align="right">  1370313.32</td>
    <td align="right">      100.00</td>
  </tr>
</table>
<br><br>
<b>Setpoint Not Met Criteria</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Setpoint Not Met Criteria-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Degrees [deltaF]</td>
  </tr>
  <tr>
    <td align="right">Tolerance for Zone Heating Setpoint Not Met Time</td>
    <td align="right">        1.01</td>
  </tr>
  <tr>
    <td align="right">Tolerance for Zone Cooling Setpoint Not Met Time</td>
    <td align="right">        1.01</td>
  </tr>
</table>
<br><br>
<b>Comfort and Setpoint Not Met Summary</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Comfort and Setpoint Not Met Summary-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">Facility [Hours]</td>
  </tr>
  <tr>
    <td align="right">Time Setpoint Not Met During Occupied Heating</td>
    <td align="right">      723.00</td>
  </tr>
  <tr>
    <td align="right">Time Setpoint Not Met During Occupied Cooling</td>
    <td align="right">        0.00</td>
  </tr>
  <tr>
    <td align="right">Time Not Comfortable Based on Simple ASHRAE 55-2004</td>
    <td align="right">     6403.00</td>
  </tr>
</table>
<br><br>
Note 1: An asterisk (*) indicates that the feature is not yet implemented.<br>
<hr>
</body>
</html>
"""


# def test_gets2sconversions():
#     """py.test fro gets2sconversions"""
#     data = (
#         (
#             SampleHtml().html,
#             {
#                 "Coal": 1.05,
#                 "Diesel": 1.05,
#                 "District Cooling": 1.056,
#                 "District Heating": 3.613,
#                 "Electricity": 3.167,
#                 "Fuel Oil #1": 1.05,
#                 "Fuel Oil #2": 1.05,
#                 "Gasoline": 1.05,
#                 "Natural Gas": 1.084,
#                 "Other Fuel 1": 1.0,
#                 "Other Fuel 2": 1.0,
#                 "Propane": 1.05,
#                 "Steam": 0.3,
#             },
#         ),  # html, expected
#     )
#     for html, expected in data:
#         htables = readhtml.titletable(StringIO(html))
#         result = fasthtml.gets2sconversions(htables)
#         assert result == expected
#
#
# def test_getthetable():
#     """py.test for getthetable"""
#     data = (
#         (
#             SampleHtml().html,
#             "Site and Source Energy",
#             [
#                 [
#                     "",
#                     "Total Energy [kBtu]",
#                     "Energy Per Total Building Area [kBtu/ft2]",
#                     "Energy Per Conditioned Building Area [kBtu/ft2]",
#                 ],
#                 ["Total Site Energy", 12372300.67, 27.07, 28.11],
#                 ["Net Site Energy", 12372300.67, 27.07, 28.11],
#                 ["Total Source Energy", 31924186.59, 69.85, 72.53],
#                 ["Net Source Energy", 31924186.59, 69.85, 72.53],
#             ],
#         ),  # html, header, expected
#     )
#     for html, header, expected in data:
#         htables = readhtml.titletable(StringIO(html))
#         result = fasthtml.getthetable(htables, header)
#         assert result == expected
#


def test_getnexttable():
    """py.test for getnexttable"""
    data = (
        (
            """<!-- FullName:Adaptive Comfort Summary_Entire Facility_Time Not Meeting the Adaptive Comfort Models during Occupied Hours-->
<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">ASHRAE55 90% Acceptability Limits [Hours]</td>
  </tr>
</table>
<br><br>
""",
            """<table border="1" cellpadding="4" cellspacing="0">
  <tr><td></td>
    <td align="right">ASHRAE55 90% Acceptability Limits [Hours]</td>
  </tr>
</table>
""",
        ),  # htmltxt, expected
    )
    for htmltxt, expected in data:
        fhandle = StringIO(htmltxt)
        result = fasthtml.getnexttable(fhandle)
        assert result == expected


@pytest.mark.parametrize(
    "htmltxt, header, expected",
    [
        (
            SampleHtml().html,
            "Site to Source Energy Conversion Factors",
            [
                "Site to Source Energy Conversion Factors",
                [
                    ["", "Site=>Source Conversion Factor"],
                    ["Electricity", 3.167],
                    ["Natural Gas", 1.084],
                    ["District Cooling", 1.056],
                    ["District Heating", 3.613],
                    ["Steam", 0.3],
                    ["Gasoline", 1.05],
                    ["Diesel", 1.05],
                    ["Coal", 1.05],
                    ["Fuel Oil #1", 1.05],
                    ["Fuel Oil #2", 1.05],
                    ["Propane", 1.05],
                    ["Other Fuel 1", 1.0],
                    ["Other Fuel 2", 1.0],
                ],
            ],
        ),  # htmltxt, header, expected
    ],
)
def test_tablebyname(tmp_path, htmltxt, header, expected):
    """py.test for tablebyname"""
    fhandle = StringIO(htmltxt)
    result = fasthtml.tablebyname(fhandle, header)
    assert result == expected
    # -
    # read the html from dis in 'rb' binary mode
    tmp_file = tmp_path / "eplus.htm"
    tmp_file.write_text(htmltxt)
    fhandle = open(tmp_file, "rb")
    result = fasthtml.tablebyname(fhandle, header)
    assert result == expected


@pytest.mark.parametrize(
    "htmltxt, expected",
    [
        (
            """line1
        line2
        <table stuff>
        more stuff
        </table>
        otherstuff""",
            """line1
        line2
        <table stuff>
        more stuff
        </table>
""",
        ),  # htmltxt, expected
    ],
)
def test_get_upto_nexttable(tmp_path, htmltxt, expected):
    """py.test for get_upto_nexttable"""
    fhandle = StringIO(htmltxt)
    result = fasthtml.get_upto_nexttable(fhandle)
    assert result == expected
    tmp_file = tmp_path / "eplus.htm"
    tmp_file.write_text(htmltxt)
    fhandle = open(tmp_file, "rb")
    result = fasthtml.get_upto_nexttable(fhandle)
    # assert result == expected
    # the above line did not work on windows because of different line endings
    # so we do
    result = result.strip()
    expected = expected.strip()
    for rline, line in zip(result.splitlines(), expected.splitlines()):
        assert rline.strip() == line.strip()  # removes line endings


@pytest.mark.parametrize(
    "htmltxt, index, expected",
    [
        (
            SampleHtml().html,
            1,
            (
                "Site to Source Energy Conversion Factors",
                [
                    ["", "Site=>Source Conversion Factor"],
                    ["Electricity", 3.167],
                    ["Natural Gas", 1.084],
                    ["District Cooling", 1.056],
                    ["District Heating", 3.613],
                    ["Steam", 0.3],
                    ["Gasoline", 1.05],
                    ["Diesel", 1.05],
                    ["Coal", 1.05],
                    ["Fuel Oil #1", 1.05],
                    ["Fuel Oil #2", 1.05],
                    ["Propane", 1.05],
                    ["Other Fuel 1", 1.0],
                    ["Other Fuel 2", 1.0],
                ],
            ),
        ),  #  htmltxt, index, expected
    ],
)
def test_tablebyindex(tmp_path, htmltxt, index, expected):
    """py.test for tablebyindex"""
    fhandle = StringIO(htmltxt)
    result = fasthtml.tablebyindex(fhandle, index)
    assert result == expected
    tmp_file = tmp_path / "eplus.htm"
    tmp_file.write_text(htmltxt)
    fhandle = open(tmp_file, "rb")
    result = fasthtml.tablebyindex(fhandle, index)
    assert result == expected
